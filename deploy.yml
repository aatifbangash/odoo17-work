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
