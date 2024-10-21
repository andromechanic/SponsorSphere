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
            <router-link to="/admin/find" class="nav-link ">Find</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/stats" class="nav-link active">Stats</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  <div class="container mt-4">
    <h1 style="font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;" class="dashboard-heading">Admin Statistics</h1>

    <div class="row">
      <div class="col-md-4 mb-4">
        <div class="card total-stats-card">
          <div class="card-body">
            <h5 class="card-title">Total Statistics</h5>
            <ul class="list-group">
              <li class="list-group-item">Total Sponsors: {{ totalSponsors }}</li>
              <li class="list-group-item">Total Influencers: {{ totalInfluencers }}</li>
              <li class="list-group-item">Total Campaigns: {{ totalCampaigns }}</li>
              <li class="list-group-item">Ongoing Campaigns: {{ ongoingCampaigns }}</li>
              <li class="list-group-item">Flagged Campaigns: {{ flaggedCampaigns }}</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="col-md-8 mb-4">
        <div class="card user-stats-chart-card">
          <div class="card-body">
            <h5 class="card-title">User Statistics</h5>
            <canvas id="userStatsChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-8 mb-4">
        <div style=" height: 350px;" class="card campaign-stats-chart-card">
          <div class="card-body">
            <h5 class="card-title">Campaign Statistics</h5>
            <canvas style="max-height: 250px; width: 100% !important;height: 100% !important;" id="campaignStatsChart"></canvas>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-4">
        <div class="card top-niches-card">
          <div class="card-body">
            <h5 class="card-title">Top Niches</h5>
            <ul class="list-group">
              <li v-for="niche in topNiches" :key="niche.niche" class="list-group-item">
                {{ niche.niche }}: {{ niche.count }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: "AdminStats",
  data() {
    return {
      totalSponsors: 0,
      totalInfluencers: 0,
      totalCampaigns: 0,
      ongoingCampaigns: 0,
      flaggedCampaigns: 0,
      averageBudget: 0,
      topNiches: [],
      userStatsChart: null,
      campaignStatsChart: null
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/admin/signin');
    },
    async fetchStatistics() {
      try {
        const response = await fetch("http://127.0.0.1:5000/admin/statistics", {
          headers: {
            "Authorization": "Bearer " + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          const data = await response.json();
          this.totalSponsors = Math.floor(data.total_sponsors);
          this.totalInfluencers = Math.floor(data.total_influencers);
          this.totalCampaigns = Math.floor(data.total_campaigns);
          this.ongoingCampaigns = Math.floor(data.ongoing_campaigns);
          this.flaggedCampaigns = Math.floor(data.flagged_campaigns);
          this.averageBudget = Math.floor(data.average_budget);
          this.topNiches = data.top_niches;
          this.renderCharts();
        } else {
          console.error("Failed to fetch statistics");
        }
      } catch (error) {
        console.error("Error fetching statistics:", error);
      }
    },
    renderCharts() {
      const ctxUserStats = document.getElementById('userStatsChart').getContext('2d');
      this.userStatsChart = new Chart(ctxUserStats, {
        type: 'bar',
        data: {
          labels: ['Total Sponsors', 'Total Influencers', 'Total Campaigns'],
          datasets: [{
            label: 'User Statistics',
            data: [this.totalSponsors, this.totalInfluencers, this.totalCampaigns],
            backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'],
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1,
                callback: function(value) {
                  if (value >= 0 && value <= 4) {
                    return value;
                  }
                  return '';
                }
              }
            }
          }
        }
      });

      const ctxCampaignStats = document.getElementById('campaignStatsChart').getContext('2d');
      this.campaignStatsChart = new Chart(ctxCampaignStats, {
        type: 'pie',
        data: {
          labels: ['Flagged Campaigns', 'Non-Flagged Campaigns'],
          datasets: [{
            label: 'Campaign Statistics',
            data: [this.flaggedCampaigns, this.totalCampaigns - this.flaggedCampaigns],
            backgroundColor: ['#FF6384', '#36A2EB'],
          }]
        },
        options: {
          responsive: true,
        }
      });
    },
    destroyCharts() {
      if (this.userStatsChart) {
        this.userStatsChart.destroy();
      }
      if (this.campaignStatsChart) {
        this.campaignStatsChart.destroy();
      }
    }
  },
  mounted() {
    this.fetchStatistics();
  },
  beforeUnmount() {
    this.destroyCharts();
  }
};
</script>

<style scoped>
.dashboard-heading {
  font-family: 'Arial', sans-serif;
}
body{
  font-family: Arial, sans-serif;
  background-color: var(--light-color);
  margin: 0;
  padding: 0;
  background-color: #93bf9d;
  height: auto;
}

.card {
  border: none;
  border-radius: 10px;
  margin-bottom: 20px; 
  max-width: 1200px;
}

.total-stats-card {
  background-color: #519ce6;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

}

.user-stats-chart-card {
  background-color: #e9ecef;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.campaign-stats-chart-card {
  background-color: #f1f3f5;
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 400px;
}

.top-niches-card {
  background-color: #ffffff; 
  max-width: 1200px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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
