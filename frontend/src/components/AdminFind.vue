<template>
  <body>
    <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #06402b;" >
    <div class="container-fluid">
      <a class="navbar-brand" style="font-family: Copperplate, Papyrus, fantasy;color: azure;" href="#">Sponsor Sphere</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto"> 
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link ">Info</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/find" class="nav-link active">Find</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/stats" class="nav-link">Stats</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div class="container mt-4">
    <h2 style="font-family:Trebuchet MS, Helvetica, sans-serif;" >Find Users</h2>
    <ul class="nav nav-tabs" id="userTabs" role="tablist">
      <li class="nav-item" role="presentation">
        <button class="nav-link active" id="influencers-tab" data-bs-toggle="tab" data-bs-target="#influencers" type="button" role="tab" aria-controls="influencers" aria-selected="true">Influencers</button>
      </li>
      <li class="nav-item" role="presentation">
        <button class="nav-link" id="sponsors-tab" data-bs-toggle="tab" data-bs-target="#sponsors" type="button" role="tab" aria-controls="sponsors" aria-selected="false">Sponsors</button>
      </li>
    </ul>
    <div class="tab-content" id="userTabsContent">
      <div class="tab-pane fade show active" id="influencers" role="tabpanel" aria-labelledby="influencers-tab">
        <h3 class="mt-3">Influencers</h3>
        <ul class="list-group">
          <li v-for="influencer in influencers" :key="influencer.ID" class="list-group-item d-flex justify-content-between align-items-center">
            {{ influencer.Name }}
            <button @click="flagUser('Influencer', influencer.ID)" class="btn btn-warning btn-sm" :disabled="influencer.Flagged">
              {{ influencer.Flagged ? 'Flagged' : 'Flag' }}
            </button>
          </li>
        </ul>
      </div>
      <div class="tab-pane fade" id="sponsors" role="tabpanel" aria-labelledby="sponsors-tab">
        <h3 class="mt-3">Sponsors</h3>
        <ul class="list-group">
          <li v-for="sponsor in sponsors" :key="sponsor.ID" class="list-group-item d-flex justify-content-between align-items-center">
            {{ sponsor.Name }}
            <button @click="flagUser('Sponsor', sponsor.ID)" class="btn btn-warning btn-sm" :disabled="sponsor.Flagged">
              {{ sponsor.Flagged ? 'Flagged' : 'Flag' }}
            </button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</body>
</template>

<script>
export default {
  name: "AdminFind",
  data() {
    return {
      influencers: [],
      sponsors: [],
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/admin/signin');
    },
    async fetchUsers() {
      try {
        const response = await fetch("http://127.0.0.1:5000/admin/all-users", {
          headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          const data = await response.json();
          this.influencers = data.filter(item => item.Type === 'Influencer');
          this.sponsors = data.filter(item => item.Type === 'Sponsor');
        } else {
          console.error("Failed to fetch users");
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    async flagUser(userType, userId) {
      try {
        const itemType = userType.toLowerCase();
        const response = await fetch(`http://127.0.0.1:5000/admin/flag/${itemType}/${userId}`, {
          method: "POST",
          headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          alert(`${userType} with ID ${userId} has been flagged.`);
          const userList = userType === 'Influencer' ? this.influencers : this.sponsors;
          const user = userList.find(u => u.ID === userId);
          if (user) user.Flagged = true;
        } else {
          const errorData = await response.json();
          throw new Error(errorData.message || `Failed to flag ${userType}`);
        }
      } catch (error) {
        console.error(`Error flagging ${userType}:`, error);
        alert(`Failed to flag ${userType}: ${error.message}`);
      }
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>
<style scoped>
body{
  font-family: Arial, sans-serif;
  background-color: #93bf9d;
  margin: 0;
  padding: 0;
  height: 100vh;
}

.navbar {
  background-color: var(--primary-color);
  padding: 1rem;
  color: #f8f9fa;
}

.nav-tabs {
  border-bottom: none;
}

.nav-link {
  color: #ffffff;
  border: none;
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  background-color: rgb(255, 255, 255);
  color:black;
}
</style>