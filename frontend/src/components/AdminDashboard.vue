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
            <router-link to="/admin/dashboard" class="nav-link active">Info</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/find" class="nav-link">Find</router-link>
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
    <h1 class="dashboard-heading">Admin Dashboard</h1>
    
    
    <div class="card ongoing-campaigns-card mb-4">
      <div class="card-body">
        <h2 class="card-title">Ongoing Campaigns</h2>
        <div v-if="loading.campaigns">Loading campaigns...</div>
        <div v-else-if="error.campaigns" class="alert alert-danger">{{ error.campaigns }}</div>
        <table v-else class="table table-striped">
          <thead>
            <tr>
              <th>Campaign ID</th>
              <th>Title</th>
              <th>Sponsor</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="campaign in ongoingCampaigns" :key="campaign.CampaignID">
              <td>{{ campaign.CampaignID }}</td>
              <td>{{ campaign.Title }}</td>
              <td>{{ campaign.SponsorName }}</td>
              <td>{{ formatDate(campaign.StartDate) }}</td>
              <td>{{ formatDate(campaign.EndDate) }}</td>
              <td>{{ campaign.Status }}</td>
              <td>
                <button class="btn btn-sm btn-warning" @click="flagItem('Campaign', campaign.CampaignID)">Flag</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card flagged-users-card">
      <div class="card-body">
        <h2 class="card-title">Flagged Users and Campaigns</h2>
        <div v-if="loading.flagged">Loading flagged items...</div>
        <div v-else-if="error.flagged" class="alert alert-danger">{{ error.flagged }}</div>
        <table v-else class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>Type</th>
              <th>Name</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in flaggedItems" :key="`${item.Type}-${item.ID}`">
              <td>{{ item.ID }}</td>
              <td>{{ item.Type }}</td>
              <td>{{ item.Name }}</td>
              <td>
                <button class="btn btn-sm btn-warning" @click="unflagItem(item)">Unflag</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</body>
</template>

<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      ongoingCampaigns: [],
      flaggedItems: [],
      loading: {
        campaigns: true,
        flagged: true
      },
      error: {
        campaigns: null,
        flagged: null
      }
    };
  },
  mounted() {
    this.fetchOngoingCampaigns();
    this.fetchFlaggedItems();
  },
  methods: {
    async fetchOngoingCampaigns() {
      this.loading.campaigns = true;
      this.error.campaigns = null;
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/ongoing-campaigns', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          this.ongoingCampaigns = await response.json();
        } else {
          throw new Error('Failed to fetch ongoing campaigns');
        }
      } catch (error) {
        console.error('Error fetching ongoing campaigns:', error);
        this.error.campaigns = 'Failed to load ongoing campaigns. Please try again.';
      } finally {
        this.loading.campaigns = false;
      }
    },
    async fetchFlaggedItems() {
      this.loading.flagged = true;
      this.error.flagged = null;
      try {
        const response = await fetch('http://127.0.0.1:5000/admin/flagged-items', {
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          this.flaggedItems = await response.json();
        } else {
          throw new Error('Failed to fetch flagged items');
        }
      } catch (error) {
        console.error('Error fetching flagged items:', error);
        this.error.flagged = 'Failed to load flagged items. Please try again.';
      } finally {
        this.loading.flagged = false;
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    async flagItem(itemType, itemId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/flag/${itemType}/${itemId}`, {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          alert(`${itemType} with ID ${itemId} has been flagged.`);
          await this.fetchOngoingCampaigns();
          await this.fetchFlaggedItems();
        } else {
          throw new Error('Failed to flag item');
        }
      } catch (error) {
        console.error('Error flagging item:', error);
        alert('Failed to flag item. Please try again.');
      }
    },
    async unflagItem(item) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/admin/unflag/${item.Type}/${item.ID}`, {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          alert(`${item.Type} ${item.Name} has been unflagged.`);
          await this.fetchFlaggedItems();
        } else {
          throw new Error('Failed to unflag item');
        }
      } catch (error) {
        console.error('Error unflagging item:', error);
        alert('Failed to unflag item. Please try again.');
      }
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/admin/signin');
    }
  }
};
</script>

<style scoped>
body{
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #93bf9d;
}
.container {
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dashboard-heading {
  font-family:"Trebuchet MS", Helvetica, sans-serif; 
}

.card {
  margin-bottom: 20px; 
}

.card-title {
  font-family: "Courier New", Courier, monospace;
  font-size:30px;
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
