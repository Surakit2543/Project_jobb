<template>
    <div class="about">
        <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="title">Create course</h1>
            </div>
        </div>

        <section class="section">
            <div class="mb-6 px-6 py-4 has-background-grey-lighter">
                <h2 class="subtitle">Meta information</h2>

                <div class="field">
                    <label>Title</label>
                    <input type="text" class="input" v-model="form.title">
                </div>

                <div class="field">
                    <label>Short description</label>
                    <textarea class="textarea" v-model="form.short_description"></textarea>
                </div>

                <div class="field">
                    <label>Long description</label>
                    <textarea class="textarea" v-model="form.long_description"></textarea>
                </div>

                <div class="field">
                    <div class="select is-multiple">
                        <select multiple size="10" v-model="form.categories">
                            <option 
                                v-for="category in categories"
                                v-bind:key="category.id"
                                v-bind:value="category.id"
                            >
                                {{ category.title }}
                            </option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="mb-6 px-6 py-4 has-background-grey-lighter">
                <h2 class="subtitle">Lessons</h2>

                <div
                    v-for="(lesson, index) in form.lessons"
                    v-bind:key="index"
                    class="mb-4"
                >
                    <h3 class="subtitle is-size-6">Lesson</h3>

                    <div class="field">
                        <label>Title</label>
                        <input 
                            type="text" 
                            class="input" 
                            v-model="lesson.title"
                            :name="`form.lessons[${index}][title]`"
                        >
                    </div>

                    <div class="field">
                        <label>Short description</label>
                        <textarea class="textarea" v-model="lesson.short_description" :name="`form.lessons[${index}][short_description]`"></textarea>
                    </div>

                    <div class="field">
                        <label>Long description</label>
                        <textarea class="textarea" v-model="lesson.long_description" :name="`form.lessons[${index}][long_description]`"></textarea>
                    </div>

                    <div class="field">
                        <label>Lesson type</label><br>
                        <div class="select">
                            <select v-model="lesson.type">
                                <option 
                                    v-for="lesson in lessonType"
                                    v-bind:key="lesson"
                                    v-bind:value="lesson"
                                >
                                    {{ lesson }}
                                </option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="field" v-if="lesson.type == 'Quiz'">
                        <div>
                            <label>question</label>
                            <input 
                                type="text" 
                                class="input" 
                                v-model="lesson.quiz.question"
                                :name="`form.lessons[${index}][quiz][question]`"
                            >
                            <label>answer</label>
                            <input 
                                type="text" 
                                class="input" 
                                v-model="lesson.quiz.answer"
                                :name="`form.lessons[${index}][quiz][answer]`"
                            >
                            <label>op1</label>
                            <input 
                                type="text" 
                                class="input" 
                                v-model="lesson.quiz.op1"
                                :name="`form.lessons[${index}][quiz][op1]`"
                            >
                            <label>op2</label>
                            <input 
                                type="text" 
                                class="input" 
                                v-model="lesson.quiz.op2"
                                :name="`form.lessons[${index}][quiz][op2]`"
                            >
                            <label>op3</label>
                            <input 
                                type="text" 
                                class="input" 
                                v-model="lesson.quiz.op3"
                                :name="`form.lessons[${index}][quiz][op3]`"
                            >
                        </div>
                        
                    </div>

                    <div class="field" v-if="lesson.type == 'Video'">
                        <label>Youtube id</label>
                        <input 
                            type="text" 
                            class="input" 
                            v-model="lesson.youtube_id"
                            :name="`form.lessons[${index}][youtube_id]`"
                        >
                    </div>

                    <hr>
                </div>

                <button class="button is-primary" @click="addLesson()">Add lesson</button>
                <button class="ml-3 button is-danger" v-if="form.lessons.length > 0" @click="deleteLesson()">delete lesson</button>
            </div>

            <div class="field buttons">
                <button class="button is-success" @click="submitForm('draft')">Save as draft</button>
                <button class="button is-info" @click="submitForm('review')">Submit for review</button>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            form: {
                title: '',
                short_description: '',
                long_description: '',
                categories: [],
                status: '',//published , draft
                lessons: []
            },
            categories: [],
            lessonType: ["Article","Quiz","Video"]
        }
    },
    mounted() {
        this.getCategories()
    },
    methods: {
        getCategories() {
            console.log('getCategories')

            axios
                .get('courses/get_categories/')
                .then(response => {
                    console.log(response.data)

                    this.categories = response.data
                })
        },
        submitForm(status) {
            console.log('submitForm')
            console.log(this.form)
            
            
            status = 'published';
            this.form.status = status;
            if(this.validateError()){
                return
            }
            axios
                .post('courses/create/', this.form)
                .then(response => {
                    console.log(response.data)
                    this.$swal('Save','','success')
                        .then((result) => {
                        if (result.isConfirmed) {
                            location.reload()
                        }
                        })
                })
                .catch(error => {
                    console.log('error:', error)
                })
                
        },
        addLesson() {
            console.log('addLesson')

            this.form.lessons.push({
                title: '',
                short_description: '',
                long_description: '',
                type : 'Article',
                youtube_id : '',
                quiz:{
                    question:'',
                    answer:'',
                    op1:'',
                    op2:'',
                    op3:''
                }
            })
        },
        deleteLesson(){
            this.form.lessons.pop();
        },
        validateError(){
            var isError = false;
            if(this.form?.title == undefined || this.form?.title == ''){
                console.log('cannot submitForm')
                this.$swal('Title cannot empty','','warning');
                return true
            }
            if(this.form?.categories.length == 0){
                this.$swal('categories cannot empty','','warning');
                return true
            }
            if(this.form?.lessons?.length > 0){
                this.form?.lessons?.forEach((item)=>{
                    if(item?.title == undefined || item?.title == ''){
                        isError = true;
                    }
                })
                if(isError){
                    this.$swal('Lessons Title cannot empty','','warning');
                    return true
                }
            }
            return false
        }
    }
}
</script>