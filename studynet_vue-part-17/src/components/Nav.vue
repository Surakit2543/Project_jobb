<template>
    <nav class="navbar is-info" role="navigation" aria-label="main naviation" style="min-height: 5rem;">
        <div class="navbar-brand">
            <router-link class="navbar-item is-size-4" to="/">lll</router-link>
        </div>

        <div id="navbar-item" class="navbar-menu">
            <div class="navbar-start">
                <router-link to="/" class="navbar-item">Home</router-link>
                <router-link to="/about" class="navbar-item">Caculate</router-link>
                <router-link to="/file" class="navbar-item">File</router-link>
                <router-link to="/courses" class="navbar-item">Courses</router-link>
                
            </div>

            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons">
                        <template v-if="$store.state.user.isAuthenticated">
                            <router-link to="/dashboard/my-course" class="navbar-item button is-primary is-light">My Courses</router-link>
                            <router-link to="/dashboard/create-course/new" id="createCourseBtn" class="button is-primary">Create course</router-link>
                            <router-link to="/dashboard/my-account" class="button is-info">My account</router-link>
                        </template>

                        <template v-else>
                            <router-link to="/sign-up" class="button is-primary"><strong>Sign up</strong></router-link>
                            <router-link to="/log-in" class="button is-light">Log in</router-link>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>