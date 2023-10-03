<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">My Courses</h1>
      </div>
    </div>

    <section class="section">
      <div class="columns is-multiline">
        <div class="column is-12">
          <h2 class="subtitle is-size-3">Your courses</h2>
        </div>

        <div 
          class="column is-4"
          v-for="course in courses"
          v-bind:key="course.id"
        >
          <CourseItem :course="course" :isEdit='true' />
        </div>
      </div>

      <hr>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

import CourseItem from '@/components/CourseItem.vue'

export default {
    data() {
      return {
        courses: []
      }
    },
    components: {
      CourseItem
    },
    mounted() {
        axios
            .get('courses/get_my_courses/')
            .then(response => {
                console.log(response.data)

                this.courses = response.data
            })
    },
    methods: {
        
    }
}
</script>