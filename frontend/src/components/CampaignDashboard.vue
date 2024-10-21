<template>
  <body>
    <div>
      <div>
      <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="d-flex justify-content-between w-100">
          <span class="navbar-brand" style="font-family: Copperplate, Papyrus, fantasy;" >Sponsor Sphere</span> <!-- Added brand name -->
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <a class="nav-link " aria-current="page" href="/sponsor/dashboard">Dashboard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href='/sponsor/campaign'>Campaigns</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/sponsor/find">Find</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" @click="Logout">Logout</a>
            </li>
          </ul>
        </div>
      </nav>
    </div>

      <div style="display: flex; justify-content: space-between">
        <div style="width: 25%; padding: 20px">
          <div class="frosted-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <h3 style="color: var(--light-color);">Add Campaigns</h3>
              <button class="btn btn-custom" @click="reload" style="margin-left: 10px">+</button>
            </div>
            <form @submit.prevent="submitCampaign" class="mt-3">
              <div class="mb-2">
                <label for="title" class="form-label" style="font-size: 0.9rem">Title</label>
                <input type="text" class="form-control form-control-sm" id="title" v-model="campaign.Title" required />
              </div>
              <div class="mb-2">
                <label for="description" class="form-label" style="font-size: 0.9rem">Description</label>
                <textarea class="form-control form-control-sm" id="description" v-model="campaign.Description" rows="2" required></textarea>
              </div>
              <div class="mb-2">
                <label for="budget" class="form-label" style="font-size: 0.9rem">Budget</label>
                <input type="number" class="form-control form-control-sm" id="budget" v-model="campaign.Budget" required />
              </div>
              <div class="mb-2">
                <label for="startDate" class="form-label" style="font-size: 0.9rem">Start Date</label>
                <input type="datetime-local" class="form-control form-control-sm" id="startDate" v-model="campaign.StartDate" required />
              </div>
              <div class="mb-2">
                <label for="endDate" class="form-label" style="font-size: 0.9rem">End Date</label>
                <input type="datetime-local" class="form-control form-control-sm" id="endDate" v-model="campaign.EndDate" required />
              </div>
              <div class="mb-2">
                <label for="niche" class="form-label" style="font-size: 0.9rem">Niche</label>
                <input type="text" class="form-control form-control-sm" id="niche" v-model="campaign.Niche" required />
              </div>
              <div class="mb-2">
                <label for="goals" class="form-label" style="font-size: 0.9rem">Goals</label>
                <input type="text" class="form-control form-control-sm" id="goals" v-model="campaign.Goals" required />
              </div>
              <div class="mb-2">
                <label for="status" class="form-label" style="font-size: 0.9rem">Status</label>
                <select class="form-select form-select-sm" id="status" v-model="campaign.Status" required>
                  <option value="Active">Active</option>
                  <option value="Paused">Paused</option>
                </select>
              </div>
              <button type="submit" class="btn btn-custom btn-sm" style="width: 100%">{{ editing ? "Update" : "Submit" }}</button>
            </form>
          </div>
        </div>

        <div style="width: 75%; padding: 20px">
          <div class="frosted-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <h3 style="color: var(--light-color);">Campaigns</h3>
              <div style="width: 50%;margin-bottom: 10px;">
                <input type="text" class="form-control" placeholder="Search Campaign Name/Description" v-model="searchQuery" @input="filterCampaigns" />
              </div>
            </div>
            <div>
              <table class="table table-striped table-bordered glass-table">
                <thead>
                  <tr>
                    <th style="color: var(--light-color);">Title</th>
                    <th style="color: var(--light-color);">Description</th>
                    <th style="color: var(--light-color);">Budget</th>
                    <th style="color: var(--light-color);">Goals</th>
                    <th style="color: var(--light-color);">Start Date</th>
                    <th style="color: var(--light-color);">End Date</th>
                    <th style="color: var(--light-color);">Niche</th>
                    <th style="color: var(--light-color);">Status</th>
                    <th style="color: var(--light-color);">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="campaign in filteredCampaigns" :key="campaign.CampaignID">
                    <td>{{ campaign.Title }}</td>
                    <td>{{ campaign.Description }}</td>
                    <td>{{ campaign.Budget }}</td>
                    <td>{{ campaign.Goals }}</td>
                    <td>{{ formatDate(campaign.StartDate) }}</td>
                    <td>{{ formatDate(campaign.EndDate) }}</td>
                    <td>{{ campaign.Niche }}</td>
                    <td>{{ campaign.Status }}</td>
                    <td>
                      <div style="padding-bottom: 2px">
                        <button style="width: 75px;" class="btn btn-dark btn-sm" @click="editCampaign(campaign.CampaignID)">Edit</button>
                      </div>
                      <div style="padding-top: 2px">
                        <button style="width: 75px;" class="btn btn-danger btn-sm" @click="deleteCampaign(campaign.CampaignID)">Delete</button>
                      </div>
                      <div style="padding-top: 2px">
                        <button style="width: 75px;font-size: smaller;" class="btn btn-info btn-sm" @click="viewAds(campaign.CampaignID)">View Ads</button>
                      </div>
                      <div style="padding-top: 2px">
                        <button style="width: 75px;font-size: smaller;" class="btn btn-success btn-sm" @click="exportCampaign(campaign.CampaignID)">Export</button> <!-- Export button -->
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <div style="width: 100%; margin-top: 20px;">
        <h3 style="color: var(--light-color);">Flagged Campaigns</h3>
        <table v-if="flaggedCampaigns.length > 0" class="table table-striped table-bordered glass-table">
          <thead>
            <tr>
              <th style="color: var(--light-color);">Title</th>
              <th style="color: var(--light-color);">Description</th>
              <th style="color: var(--light-color);">Budget</th>
              <th style="color: var(--light-color);">Start Date</th>
              <th style="color: var(--light-color);">End Date</th>
              <th style="color: var(--light-color);">Niche</th>
              <th style="color: var(--light-color);">Goals</th>
              <th style="color: var(--light-color);">Status</th>
              <th style="color: var(--light-color);">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="campaign in flaggedCampaigns" :key="campaign.CampaignID">
              <td>{{ campaign.Title }}</td>
              <td>{{ campaign.Description }}</td>
              <td>{{ campaign.Budget }}</td>
              <td>{{ formatDate(campaign.StartDate) }}</td>
              <td>{{ formatDate(campaign.EndDate) }}</td>
              <td>{{ campaign.Niche }}</td>
              <td>{{ campaign.Goals }}</td>
              <td>{{ campaign.Status }}</td>
              <td>
                <button class="btn btn-warning btn-sm" @click="contactAdmin(campaign.CampaignID)">Contact Admin</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else style="color: var(--light-color);">No flagged campaigns found.</p>
      </div>
    </div>
  </body>
</template>

<script>
export default {
  data() {
    return {
      allcampaign: [],
      filteredCampaigns: [], 
      token: localStorage.getItem("jwt_token"),
      User: localStorage.getItem("auth"),
      SponsorID: localStorage.getItem("SponsorID"),
      editing: false,
      campaign: {
        Title: "",
        Description: "",
        Budget: 0,
        StartDate: "",
        EndDate: "",
        Niche: "",
        Goals: "",
        Status: "Active",
      },
      searchQuery: "", 
      flaggedCampaigns: [],
    };
  },
  methods: {
    Logout() {
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('userData');
      this.$router.push('/');
    },
    viewAds(campaignId) {
      this.$router.push(`/viewads/${campaignId}`);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString(); 
    },
    reload() {
      window.location.reload();
    },
    getallcampaigns() {
      fetch("http://127.0.0.1:5000/campaign", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + this.token,
          UserAuth: this.User,
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          this.allcampaign = Array.isArray(data) ? data : [];
          this.filteredCampaigns = this.allcampaign;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    filterCampaigns() {
      const query = this.searchQuery.toLowerCase();
      this.filteredCampaigns = this.allcampaign.filter(campaign => 
        campaign.Title.toLowerCase().includes(query) || 
        campaign.Description.toLowerCase().includes(query)
      );
    },
    async submitCampaign() {
      if (this.editing) {
        await this.updateCampaign();
      } else {
        try {
          const response = await fetch("http://127.0.0.1:5000/campaign", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: "Bearer " + this.token,
            },
            body: JSON.stringify(this.campaign),
          });
          if (response.ok) {
            const newCampaign = await response.json();
            this.allcampaign.push(newCampaign);
            this.filteredCampaigns.push(newCampaign);
            this.resetForm();
          }
        } catch (error) {
          console.log(error);
        }
      }
    },
    resetForm() {
      this.campaign = {
        Title: "",
        Description: "",
        Budget: 0,
        StartDate: "",
        EndDate: "",
        Niche: "",
        Goals: "",
        Status: "Active",
      };
      this.editing = false;
    },
    async editCampaign(campaignID) {
      const campaignToEdit = this.allcampaign.find(c => c.CampaignID === campaignID);
      if (campaignToEdit) {
        this.campaign = { ...campaignToEdit };
        this.editing = true;
      }
    },
    async updateCampaign() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/campaign/${this.campaign.CampaignID}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.token,
          },
          body: JSON.stringify(this.campaign),
        });
        if (response.ok) {
          const updatedCampaign = await response.json();
          const index = this.allcampaign.findIndex(c => c.CampaignID === updatedCampaign.CampaignID);
          this.$set(this.allcampaign, index, updatedCampaign);
          const filteredIndex = this.filteredCampaigns.findIndex(c => c.CampaignID === updatedCampaign.CampaignID);
          this.$set(this.filteredCampaigns, filteredIndex, updatedCampaign);
          this.resetForm();
        }
      } catch (error) {
        console.log(error);
      }
    },
    async deleteCampaign(campaignID) {
      const confirmDelete = confirm("Are you sure you want to delete this campaign?");
      if (confirmDelete) {
        try {
          const response = await fetch(`http://127.0.0.1:5000/campaign/${campaignID}`, {
            method: "DELETE",
            headers: {
              Authorization: "Bearer " + this.token,
            },
          });
          if (response.ok) {
            this.allcampaign = this.allcampaign.filter(c => c.CampaignID !== campaignID);
            this.filteredCampaigns = this.filteredCampaigns.filter(c => c.CampaignID !== campaignID);
          }
        } catch (error) {
          console.log(error);
        }
      }
    },
    async getFlaggedCampaigns() {
      try {
        const response = await fetch("http://127.0.0.1:5000/sponsor/flagged-campaigns", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + this.token,
          },
        });
        if (response.ok) {
          const data = await response.json();
          this.flaggedCampaigns = Array.isArray(data) ? data : [];
        } else {
          console.error("Failed to fetch flagged campaigns");
        }
      } catch (error) {
        console.error("Error fetching flagged campaigns:", error);
      }
    },
    contactAdmin(campaignId) {
      alert(`Contact admin at admin@sponsorsphere.com and mention your Campaign ID: ${campaignId}`);
    },
    async exportCampaign(campaignID) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/export-campaign-csv/${campaignID}`, {
          method: "GET",
          headers: {
            Authorization: "Bearer " + this.token,
          },
        });
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `campaign_${campaignID}.csv`; 
          document.body.appendChild(a);
          a.click();
          a.remove();
        } else {
          console.error("Failed to export campaign");
        }
      } catch (error) {
        console.error("Error exporting campaign:", error);
      }
    },
  },
  mounted() {
    this.getallcampaigns();
    this.getFlaggedCampaigns();
  },
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: var(--light-color);
  margin: 0;
  padding: 0;
  background-color: #1185be;
}

.frosted-card {
  background: rgba(255, 255, 255, 0.7); 
  backdrop-filter: blur(1px);
  border-radius: 10px; 
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2)
}

.glass-table {
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(100%);
  border-radius: 10px;
}

.table th,
.table td {
  color: rgb(0, 0, 0);
}

.table th {
  background-color: #1185be; 
  color: white; 
}

h3 {
  color: rgb(15, 15, 15);
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
  color: var(--light-color);
  border: none;
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  color: var(--light-color);
}
</style>
