/** @odoo-module **/

import { registry } from '@web/core/registry';
const { Component, useState, onWillStart, useRef } = owl;
import { useService } from "@web/core/utils/hooks";

export class OwlTodoList extends Component {
    setup(){
        this.state = useState({
            task:{name:"", color:"#FF0000", completed:false},
            optionSet:[
                {id: 1, name: '2nd Floor Rear Structural Option Location 1', enabled: true, children: [{id:1, name: 'Covered Deck 4', price: '$40', enabled: true}, {id: 2,name: 'Deck 4', price: '$10', locked:true,enabled: true}]},
                {id: 2, name: 'Rear Structural Option Location 2', enabled: true, children: [{id: 3, name: 'Deck 2', price: '$39', enabled: true}, {id:4, name: 'Courtyard 1 (Lilac Only)', price: '$72', enabled: true}]},
                {id: 3,name: 'Rear Structural Option Location 3', enabled: true, children: [{id:5,name: 'Sunroom', price: '$13', enabled: true}]}
            ],
            isEdit: false,
            activeId: false,
        })
        this.orm = useService("orm")
        this.model = "owl.todo.list"
        this.searchInput = useRef("search-input")

        onWillStart(async ()=>{
            await this.getAllTasks()
        })
    }

    async getAllTasks(){
//        this.state.optionSet = await this.orm.searchRead(this.model, [], ["name", "color", "completed"])
    }

    addTask(){
        this.resetForm()
        this.state.activeId = false
        this.state.isEdit = false
    }

    editTask(task){
        this.state.activeId = task.id
        this.state.isEdit = true
        this.state.task = {...task}
    }

    async saveTask(){

        if (!this.state.isEdit){
            await this.orm.create(this.model, [this.state.task])
            this.resetForm()
        } else {
            await this.orm.write(this.model, [this.state.activeId], this.state.task)
        }

        await this.getAllTasks()
    }

    resetForm(){
        this.state.task = {name:"", color:"#FF0000", completed:false}
    }

    toggleParentAndChildren(parentTask) {
        parentTask.enabled = !parentTask.enabled;

        parentTask.children.forEach(child => {
            child.enabled = parentTask.enabled;
        });
    }

    toggleChildAndParent(childTask, parentTask) {
        childTask.enabled = !childTask.enabled;
        //below is situation for unchecking parent on either child unchecked
        //        const allChildrenChecked = parentTask.children.every(child => child.enabled);
        //        parentTask.enabled = allChildrenChecked;
        //above is situation for unchecking parent on either child unchecked

        const allChildrenChecked = parentTask.children.every(child => child.enabled);
        const anyChildChecked = parentTask.children.some(child => child.enabled);
        parentTask.enabled = anyChildChecked || allChildrenChecked;
    }

    async deleteTask(task){
        await this.orm.unlink(this.model, [task.id])
        await this.getAllTasks()
    }

    async searchTasks(){
        const text = this.searchInput.el.value
        this.state.optionSet = await this.orm.searchRead(this.model, [['name','ilike',text]], ["name", "color", "completed"])
    }

    async toggleTask(e, task){
        await this.orm.write(this.model, [task.id], {completed: e.target.checked})
        await this.getAllTasks()
    }

    async updateColor(e, task){
        await this.orm.write(this.model, [task.id], {color: e.target.value})
        await this.getAllTasks()
    }
}

OwlTodoList.template = 'owl.TodoList'
registry.category('actions').add('owl.action_todo_list_js', OwlTodoList);