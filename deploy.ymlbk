name: Test and deploy to Amazon ECS

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
    
# default Global ENV varialbes
env:
  AWS_REGION: eu-west-1 # set this to your preferred AWS region, e.g. us-west-1
  ECR_REPOSITORY: orangutan # set this to your Amazon ECR repository name
  ECS_SERVICE: orangutancluster-service # set this to your Amazon ECS service name
  ECS_CLUSTER: OrangutanCluster # set this to your Amazon ECS cluster name
  ECS_TASK_DEFINITION: ./task_definition.json # set this to the path to your Amazon ECS task definition file, e.g. .aws/task-definition.json
  CONTAINER_NAME: orangutancluster-container # set this to the name of the container in the containerDefinitions section of your task definition

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    - name: Build and test
      uses: gradle/gradle-build-action@937999e9cc2425eddc7fd62d1053baf041147db7
      with:
        arguments: build
        gradle-version: 7.3

  deploy:
    name: Deploy
    runs-on: self-hosted
    needs: build
    if: github.ref == 'refs/heads/master'
    # environment: production

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          # Build a docker container and push it to ECR so that it can be deployed to ECS.
          docker build \
          -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
          docker push -a $ECR_REGISTRY/$ECR_REPOSITORY
          echo "::set-output name=image::$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"
        # ::set-output name=image::$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ====> to set the step variable
      - name: Add Account Id to task execution role arn
        run: sed -i "s/<AWS_ACCOUNT_ID>/${{secrets.AWS_ACCOUNT_ID}}/g" task_definition.json
      - name: Add Server Port
        run: sed -i "s/<SERVER_PORT>/${{secrets.SERVER_PORT}}/g" task_definition.json
      - name: Add Master DB URL
        run: sed -i "s#<MASTER_DATASOURCE_URL>#${{secrets.MASTER_DATASOURCE_URL}}#g" task_definition.json
      - name: Add Master DB Username
        run:  sed -i "s/<MASTER_DATASOURCE_USERNAME>/${{secrets.MASTER_DATASOURCE_USERNAME}}/g" task_definition.json
      - name: Add Master DB Password
        run: sed -i "s/<MASTER_DATASOURCE_PASSWORD>/${{secrets.MASTER_DATASOURCE_PASSWORD}}/g" task_definition.json
      - name: Add Stats DB port
        run: sed -i "s/<CLICK_PORT>/${{secrets.CLICK_PORT}}/g" task_definition.json
      - name: Add Stats DB Host
        run: sed -i "s/<CLICK_HOST>/${{secrets.CLICK_HOST}}/g" task_definition.json
      - name: Add Stats DB Name
        run: sed -i "s/<CLICK_DB>/${{secrets.CLICK_DB}}/g" task_definition.json
      - name: Add AMQP Host
        run: sed -i "s/<AMQP_HOST>/${{secrets.AMQP_HOST}}/g" task_definition.json
      - name: Add AMQP Port
        run: sed -i "s/<AMQP_PORT>/${{secrets.AMQP_PORT}}/g" task_definition.json
      - name: Add AMQP Username
        run: sed -i "s/<AMQP_USERNAME>/${{secrets.AMQP_USERNAME}}/g" task_definition.json
      - name: Add AMQP Password
        run: sed -i "s/<AMQP_PASSWORD>/${{secrets.AMQP_PASSWORD}}/g" task_definition.json
      - name: Add AMQP Enable SSL
        run: sed -i "s/<AMQP_ENABLE_SSL>/${{secrets.AMQP_ENABLE_SSL}}/g" task_definition.json
      - name: Add SQUIRREL URL
        run: sed -i "s#<SQUIRREL_URL>#${{secrets.SQUIRREL_URL}}#g" task_definition.json
      - name: Add HUB SPOT KEY
        run: sed -i "s/<HUB_SPOT_KEY>/${{secrets.HUB_SPOT_KEY}}/g" task_definition.json
      - name: Add HUB SPOT URL
        run: sed -i "s#<HUB_SPOT_URL>#${{secrets.HUB_SPOT_URL}}#g" task_definition.json

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: ${{ env.ECS_TASK_DEFINITION }}
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
