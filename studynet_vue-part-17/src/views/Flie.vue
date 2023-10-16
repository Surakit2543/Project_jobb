<template>
  <div class="about">
    <div class="hero is-info">
      <div class="hero-body has-text-centered">
        <h1 class="title">File</h1>
      </div>
    </div>

    <section class="section">
      <div class="columns is-multiline">
        <div class="column is-3" v-for="file in Files" v-bind:key="file.id">
          <div class="card">
            <div class="card-image">
              <figure class="image is-4by3">
                <img v-if="!file.notCorrect" :src="file.get_file" alt="Placeholder image" />
                <img v-if="file.notCorrect && ['pdf'].includes(file.fileType)" src="../assets/pdf.webp">
                <img v-if="file.notCorrect && ['docm','docx'].includes(file.fileType)" src="../assets/word.png">
                <img v-if="file.notCorrect && ['pptx'].includes(file.fileType)" src="../assets/pptx.png">
                <img v-if="file.notCorrect && ['xls','xlc','xlsx'].includes(file.fileType)" src="../assets/excel.png">
                <img v-if="file.notCorrect && !['pdf','xls','xlc','xlsx','docm','docx','pptx'].includes(file.fileType)" src="../assets/file.png">
              </figure>
            </div>

            <div class="card-content">
              <div class="media">
                <div class="media-content">
                  <p class="is-size-5">{{ file.name }}</p>
                </div>
              </div>

              <div class="content">
                <p>{{ file.description }}</p>
              </div>
              <button class="button is-info mr-2" @click="DownloadFile(file)">
                Download
              </button>
              <button
                class="button is-danger mr-2"
                style="float: right"
                @click="DeleteFile(file.id)"
              >
                delete
              </button>
              <button
                class="button is-primary mr-2"
                style="float: right"
                @click="EditFile(file)"
              >
                edit
              </button>
            </div>
          </div>

          <!-- <embed :src="file.get_file" type="application/pdf" width="100%" height="500px" /> -->
        </div>
      </div>
      <button class="button is-primary mr-2" @click="AddFile()">Add</button>
    </section>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      newFile: {
        name: "",
        file: null,
      },
      Files: null,
    };
  },
  async mounted() {
    document.title = "About | StudyNet";
    axios.get("courses/get_file/").then((response) => {
      console.log(response.data);
      this.Files = response.data;
      this.Files.forEach(item => {
        console.log(window.location.host)
        if(["pdf","docm","docx","xlsx","pttx"].includes(this.getFileType(item.get_file))){
          item.notCorrect = true;
          item.fileType = this.getFileType(item.get_file)
        }
      });
    });
  },
  methods: {
    AddFile() {
      this.$swal
        .fire({
          title: "Add File",
          text: "Modal with a custom image.",
          html: `<label>File</label>
          <input
            type="file"
            id="fileInput"
            name="file"
          />
          <p>File Name</p>
          <input autocapitalize="off" class="swal2-input" id="FileName" style="width:23rem;" placeholder="" type="text">
          <p>File Description</p>
          <input autocapitalize="off" class="swal2-input" id="FileDescription" style="width:23rem;" placeholder="" type="text">
          `,
        })
        .then((result) => {
          this.$swal.showLoading();
          if (result.isConfirmed) {
            var file = document.querySelector("#fileInput");
            var fileName = document.getElementById("FileName").value;
            var fileDescription =
              document.getElementById("FileDescription").value;
            const formData = new FormData();
            formData.append("name", fileName);
            formData.append("description", fileDescription);
            formData.append("file", file.files[0]);
            axios
              .post("courses/create_file/", formData, {
                headers: {
                  "Content-Type": "multipart/form-data", // Important for file uploads
                },
              })
              .then((response) => {
                console.log(response.data);
                this.$swal("create", "", "success").then((result) => {
                  location.reload();
                });
              })
              .catch((error) => {
                console.log("error:", error);
              });
          }
        });
    },
    handleFileChange(event) {
      this.newFile.file = event.target.files[0];
      const fileInput = event.target;
      const selectedFile = fileInput.files[0];
    },
    DeleteFile(fileId) {
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
              .delete(`courses/delete_file/${fileId}`)
              .then((response) => {
                this.$swal
                  .fire({
                    title: "Deleted!",
                    text: "Your file has been deleted.",
                    icon: "success",
                    didClose: () => {
                      location.reload();
                    },
                  })
                  .then((result) => {
                    location.reload();
                  });
              })
              .catch((error) => {
                console.log("error:", error);
              });
          }
        });
    },
    EditFile(file) {
      this.$swal
        .fire({
          title: "Edit File",
          text: "Modal with a custom image.",
          html: `
          <p>File Name</p>
          <input autocapitalize="off" value="${file.name}" class="swal2-input" id="editFileName" style="width:23rem;" placeholder="" type="text">
          <p>File Description</p>
          <input autocapitalize="off" value="${file.description}" class="swal2-input" id="editFileDescription" style="width:23rem;" placeholder="" type="text">
          `,
        })

        .then((result) => {
          this.$swal.showLoading();
          if (result.isConfirmed) {
            var fileName = document.getElementById("editFileName").value;
            var fileDescription = document.getElementById(
              "editFileDescription"
            ).value;
            const formData = new FormData();
            formData.append("name", fileName);
            formData.append("description", fileDescription);
            axios
              .put(`courses/edit_file/${file.id}`, formData, {
                headers: {
                  "Content-Type": "multipart/form-data", // Important for file uploads
                },
              })
              .then((response) => {
                console.log(response.data);
                this.$swal("Save", "", "success").then((result) => {
                  location.reload();
                });
              })
              .catch((error) => {
                console.log("error:", error);
              });
          }
        });
    },
    // DownloadFile(file) {
    //   var fileType = this.getFileType(file.get_file);
    //   const a = document.createElement("a");
    //   a.href = file.get_file;
    //   a.download = `${file.name}.${fileType}`;
    //   a.style.display = "none";
    //   document.body.appendChild(a);
    //   a.click();
    //   document.body.removeChild(a);
    // },
    DownloadFile(file) {
      var fileType = this.getFileType(file.get_file);
      axios
        .get(`courses/download_file/${file.id}`, { responseType: "blob" })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", `${file.name}.${fileType}`); // Adjust the filename
          document.body.appendChild(link);
          link.click();
        });
    },
    getFileType(fileName) {
      return fileName.split(".").pop().toLowerCase();
    },
  },
};
</script>