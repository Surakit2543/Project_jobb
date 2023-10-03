<style>
.resized-image {
    max-width: 500px;
    max-height: 500px;
  }
</style>
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
          <input type="text" class="input" v-model="form.title" />
        </div>

        <div class="field">
          <label>Short description</label>
          <textarea
            class="textarea"
            v-model="form.short_description"
          ></textarea>
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

        <div class="field">
          <label>Image(.jpg, .jpeg, .png)</label>
          <input
            type="file"
            id="fileInput"
            name="file"
            accept=".jpg, .jpeg, .png"
            @change="handleFileChange"
          />
          <figure class="image  resized-image">
                <img :src="form.get_image" alt="Placeholder image" class="resized-image">
            </figure>
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
            />
          </div>

          <div class="field">
            <label>Short description</label>
            <textarea
              class="textarea"
              v-model="lesson.short_description"
              :name="`form.lessons[${index}][short_description]`"
            ></textarea>
          </div>

          <div class="field">
            <label>Long description</label>
            <textarea
              class="textarea"
              v-model="lesson.long_description"
              :name="`form.lessons[${index}][long_description]`"
            ></textarea>
          </div>

          <div class="field">
            <label>Lesson type</label><br />
            <div class="select">
              <select v-model="lesson.lesson_type">
                <option
                  v-for="lType in lessonType"
                  v-bind:key="lType"
                  v-bind:value="lType"
                  @change="changeLessonType(lesson, lType)"
                >
                  {{ lType }}
                </option>
              </select>
            </div>
          </div>

          <div class="field" v-if="lesson.lesson_type == 'quiz'">
            <div>
              <label>question</label>
              <input
                type="text"
                class="input"
                v-model="lesson.quiz.question"
                :name="`form.lessons[${index}][quiz][question]`"
              />
              <label>answer</label>
              <input
                type="text"
                class="input"
                v-model="lesson.quiz.answer"
                :name="`form.lessons[${index}][quiz][answer]`"
              />
              <label>op1</label>
              <input
                type="text"
                class="input"
                v-model="lesson.quiz.op1"
                :name="`form.lessons[${index}][quiz][op1]`"
              />
              <label>op2</label>
              <input
                type="text"
                class="input"
                v-model="lesson.quiz.op2"
                :name="`form.lessons[${index}][quiz][op2]`"
              />
              <label>op3</label>
              <input
                type="text"
                class="input"
                v-model="lesson.quiz.op3"
                :name="`form.lessons[${index}][quiz][op3]`"
              />
            </div>
          </div>

          <div class="field" v-if="lesson.lesson_type == 'video'">
            <label>Youtube id</label>
            <input
              type="text"
              class="input"
              v-model="lesson.youtube_id"
              :name="`form.lessons[${index}][youtube_id]`"
            />
          </div>

          <hr />
        </div>

        <button class="button is-primary" @click="addLesson()">
          Add lesson
        </button>
        <button
          class="ml-3 button is-danger"
          v-if="form.lessons.length > 0"
          @click="deleteLesson()"
        >
          delete lesson
        </button>
      </div>

      <div class="field buttons">
        <button
          v-if="!isEdit"
          class="button is-success"
          @click="submitForm('review')"
        >
          Create
        </button>
        <button v-if="isEdit" class="button is-success" @click="editForm()">
          save
        </button>
        <button
          v-if="isEdit"
          class="button is-danger is-pulled-right"
          @click="deleteForm()"
        >
          delete
        </button>
      </div>
    </section>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      form: {
        title: "",
        short_description: "",
        long_description: "",
        categories: [],
        status: "", //published , draft
        lessons: [],
        Image: null,
      },
      categories: [],
      lessonType: ["article", "quiz", "video"],
      isEdit: false,
    };
  },
  async mounted() {
    this.getCategories();
    const slug = this.$route.params.slug;
    if (slug != "new") {
      this.isEdit = true;
      console.log("get courses");
      await axios.get(`courses/${slug}/`).then((response) => {
        console.log(response.data);

        this.form = response.data.course;
        this.form.lessons = response.data.lessons;

        this.form.lessons.forEach(async (item) => {
          item.quiz = {
            question: "",
            answer: "",
            op1: "",
            op2: "",
            op3: "",
          };
          if (item.lesson_type == "quiz") {
            console.log(item);
            var newquiz = await axios.get(
              `courses/${response.data.course.slug}/${item.slug}/get-quiz/`
            );
            console.log("response");
            console.log(newquiz);
            item.quiz = newquiz.data;
            console.log("item quiz");
            console.log(item.quiz);
          }
        });
      });
    } else {
      console.log("new new new");
    }
  },
  methods: {
    getCategories() {
      console.log("getCategories");

      axios.get("courses/get_categories/").then((response) => {
        console.log(response.data);

        this.categories = response.data;
      });
    },
    submitForm(status) {
      console.log("submitForm");
      console.log(this.form);
      status = "published";
      this.form.status = status;
      this.form.title = this.form.title.trim();
      const formData = new FormData();
      formData.append('title', this.form.title);
      formData.append('short_description', this.form.short_description);
      formData.append('long_description', this.form.long_description);
      formData.append('categories', this.form.categories.join(',')); // Assuming categories is an array
      formData.append('status', this.form.status);
      formData.append('lessons', JSON.stringify(this.form.lessons)); // Assuming lessons is an array
      formData.append('image', formData);
      if (this.validateError()) {
        return;
      }
      axios
        .post("courses/create/", this.form, {
          headers: {
            "Content-Type": "multipart/form-data", // Important for file uploads
          },
        })
        .then((response) => {
          console.log(response.data);
          this.$swal("create", "", "success").then((result) => {
            if (result.isConfirmed) {
              location.reload();
            }
          });
        })
        .catch((error) => {
          console.log("error:", error);
        });
    },
    editForm() {
      const formData = new FormData();
      formData.append('title', this.form.title.trim());
      formData.append('short_description', this.form.short_description);
      formData.append('long_description', this.form.long_description);
      formData.append('categories', this.form.categories.join(',')); // Assuming categories is an array
      formData.append('status', this.form.status);
      formData.append('lessons', JSON.stringify(this.form.lessons)); // Assuming lessons is an array
      formData.append('image', this.form.Image);
      axios
        .put(`courses/edit/${this.form.id}`, formData, {
          headers: {
            "Content-Type": "multipart/form-data", // Important for file uploads
          },
        })
        .then((response) => {
          console.log(response.data);
          this.$swal("save", "", "success").then((result) => {
            if (result.isConfirmed) {
              location.reload();
            }
          });
        })
        .catch((error) => {
          console.log("error:", error);
        });
    },
    deleteForm() {
      console.log(this.form);
      this.$swal
        .fire({
          title: "Are you sure?",
          text: "You won't be able to revert this!",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Yes, delete it!",
        })
        .then((result) => {
          if (result.isConfirmed) {
            axios
              .delete(`courses/delete/${this.form.id}`)
              .then((response) => {
                this.$swal
                  .fire({
                    title: "Deleted!",
                    text: "Your file has been deleted.",
                    icon: "success",
                    didClose: () => {
                      this.$router.replace({ path: "/home", replace: true });
                    },
                  })
                  .then((result) => {
                    if (result.isConfirmed) {
                      this.$router.replace({ path: "/home", replace: true });
                    }
                  });
              })
              .catch((error) => {
                console.log("error:", error);
              });
          }
        });
    },
    addLesson() {
      console.log("addLesson");
      this.form.lessons.push({
        title: "",
        short_description: "",
        long_description: "",
        lesson_type: "article",
        youtube_id: "",
        quiz: {
          question: "",
          answer: "",
          op1: "",
          op2: "",
          op3: "",
        },
      });
    },
    deleteLesson() {
      this.form.lessons.pop();
    },
    validateError() {
      var isError = false;
      if (this.form?.title == undefined || this.form?.title == "") {
        console.log("cannot submitForm");
        this.$swal("Title cannot empty", "", "warning");
        return true;
      }
      if (this.form?.categories.length == 0) {
        this.$swal("categories cannot empty", "", "warning");
        return true;
      }
      if (this.form?.lessons?.length > 0) {
        this.form?.lessons?.forEach((item) => {
          if (item?.title == undefined || item?.title == "") {
            isError = true;
          }
        });
        if (isError) {
          this.$swal("Lessons Title cannot empty", "", "warning");
          return true;
        }
      }
      return false;
    },
    changeLessonType(lesson, type) {
      console.log("changeLessonType");
      console.log(lesson);
      if (type == "quiz") {
        lesson.quiz = {
          question: "",
          answer: "",
          op1: "",
          op2: "",
          op3: "",
        };
      }
    },
    handleFileChange(event) {
      this.form.Image = event.target.files[0];
      const fileInput = event.target;
      const selectedFile = fileInput.files[0];

      if (selectedFile) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.form.get_image = e.target.result; // Update the form.get_image property
        };
        reader.readAsDataURL(selectedFile);
      } else {
        this.form.get_image = null; // Reset the form.get_image property if no file selected
      }
    },
  },
};
</script>