<template>
  <body>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
      <a class="navbar-brand" style="font-family: Copperplate, Papyrus, fantasy;" href="#">Sponsor Sphere</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/influencer/dashboard" class="nav-link active" aria-current="page">My Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/influencer/find" class="nav-link">Find Ads</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="container mt-4">
    <div class="glass-effect">
      <h1 class="text" style="margin-left: 50px;">Influencer Profile</h1>
      <div class="row">
        <div class="col-md-4">
          <div v-if="isViewing" class="text-center mb-4">
            <img :src="profile.ProfilePic || require('@/assets/noprofile.jpg')" alt="Profile Picture"
              class="img-fluid rounded-circle profile-pic mb-3">
            <h2>{{ profile.UserName }}</h2>
            <p><strong>Email:</strong> {{ profile.Email }}</p>
            <p><strong>Platforms:</strong> {{ profile.Platforms }}</p>
            <p><strong>Niche:</strong> {{ profile.Niche }}</p>
            <p><strong>Followers:</strong> {{ profile.Followers }}</p>
            <p><strong>Reach:</strong> {{ profile.Reach }}</p>
            <p><strong>Average Rating:</strong>
              {{ averageRating !== null ? `${averageRating.toFixed(2)} (${ratingCount} ratings)` : 'No ratings yet' }}
            </p>
            <button class="btn btn-primary" @click="toggleViewEdit">Edit Profile</button>
          </div>

          <div v-else>
            <h2 class="text-center mb-4">Edit Profile</h2>
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label for="username" class="form-label">Username:</label>
                <input type="text" v-model="profile.UserName" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" v-model="profile.Email" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="platforms" class="form-label">Platforms:</label>
                <input type="text" v-model="profile.Platforms" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="niche" class="form-label">Niche:</label>
                <input type="text" v-model="profile.Niche" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="followers" class="form-label">Followers:</label>
                <input type="number" v-model="profile.Followers" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="reach" class="form-label">Reach:</label>
                <input type="number" v-model="profile.Reach" class="form-control" required />
              </div>
              <div class="mb-3">
                <label for="profilePic" class="form-label">Upload Profile Picture:</label>
                <input type="file" @change="onFileChange" class="form-control" />
              </div>
              <div class="text-center">
                <button type="submit" class="btn btn-success me-2">Save Changes</button>
                <button type="button" class="btn btn-secondary" @click="toggleViewEdit">Cancel</button>
              </div>
            </form>
          </div>
        </div>
        <div class="col-md-8">
          <h3 class="mb-3">Accepted Ads</h3>
          <div v-if="acceptedAds.length > 0">
            <div class="table-responsive">
              <table class="table table-striped table-bordered glass-table">
                <thead>
                  <tr>
                    <th>Request ID</th>
                    <th>Campaign</th>
                    <th>Advertisement</th>
                    <th>Proposed Amount</th>
                    <th>Negotiated Amount</th>
                    <th>Date Requested</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ad in acceptedAds" :key="ad.RequestID">
                    <td>{{ ad.RequestID }}</td>
                    <td>{{ ad.Campaign }}</td>
                    <td>{{ ad.Advertisement }}</td>
                    <td>{{ ad['Proposed Amount'] }}</td>
                    <td>{{ ad['Negotiated Amount'] }}</td>
                    <td>{{ new Date(ad['Date Requested']).toLocaleString() }}</td>
                    <td>{{ ad.Status }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else>
            <p>No accepted ads found.</p>
          </div>

          <h3 class="mt-4 mb-3">Pending Ad Requests</h3>
          <div v-if="pendingAds.length > 0">
            <div class="table-responsive">
              <table class="table table-striped table-bordered glass-table">
                <thead>
                  <tr>
                    <th>Request ID</th>
                    <th>Campaign</th>
                    <th>Advertisement</th>
                    <th>Proposed Amount</th>
                    <th>Negotiated Amount</th>
                    <th>Date Requested</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in pendingAds" :key="request.RequestID">
                    <td>{{ request.RequestID }}</td>
                    <td>{{ request.Campaign }}</td>
                    <td>{{ request.Advertisement }}</td>
                    <td>{{ request['Proposed Amount'] }}</td>
                    <td>{{ request['Negotiated Amount'] }}</td>
                    <td>{{ new Date(request['Date Requested']).toLocaleString() }}</td>
                    <td>{{ request.Status }}</td>
                    <td>
                      <div v-if="request.ReceiverInfluencerID === null && request.NegotiatedBy === 'Sponsor'">
                        <button class="btn btn-primary btn-sm me-1" @click="takeAction(request.RequestID, 'accept')">
                          Accept
                        </button>
                        <button class="btn btn-danger btn-sm" @click="takeAction(request.RequestID, 'decline')">
                          Reject
                        </button>
                      </div>
                      <button class="btn btn-warning btn-sm" @click="openNegotiationModal(request)"
                        :disabled="request.Status !== 'Pending'">
                        Negotiate
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else>
            <p>No pending ad requests found.</p>
          </div>

          <h3 class="mt-4 mb-3">Received Ad Requests</h3>
          <div v-if="recievedAds.length > 0">
            <div class="table-responsive">
              <table class="table table-striped table-bordered glass-table">
                <thead>
                  <tr>
                    <th>Request ID</th>
                    <th>Campaign</th>
                    <th>Advertisement</th>
                    <th>Proposed Amount</th>
                    <th>Negotiated Amount</th>
                    <th>Date Requested</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in recievedAds" :key="request.RequestID">
                    <td>{{ request.RequestID }}</td>
                    <td>{{ request.Campaign }}</td>
                    <td>{{ request.Advertisement }}</td>
                    <td>{{ request['Proposed Amount'] }}</td>
                    <td v-if="request.NegotiatedBy === 'Sponsor'">{{ request['Negotiated Amount'] }}</td>
                    <td v-else>N/A</td>
                    <td>{{ new Date(request['Date Requested']).toLocaleString() }}</td>
                    <td>{{ request.Status }}</td>
                    <td>
                      <button class="btn btn-primary btn-sm me-1" @click="takeAction(request.RequestID, 'accept')"
                        :disabled="request.Status !== 'Pending'">
                        Accept
                      </button>
                      <button class="btn btn-danger btn-sm" @click="takeAction(request.RequestID, 'decline')"
                        :disabled="request.Status !== 'Pending'">
                        Reject
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div v-else>
            <p>No received ad requests.</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="modal fade" id="negotiationModal" tabindex="-1" aria-labelledby="negotiationModalLabel"
    aria-hidden="true" style="color: black;">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="negotiationModalLabel">Negotiate Request</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="negotiationAmount" class="form-label">Counter Offer Amount</label>
            <input type="number" class="form-control" id="negotiationAmount" v-model="negotiationAmount">
          </div>
          <div class="mb-3">
            <label for="negotiationMessage" class="form-label">Message (Optional)</label>
            <textarea class="form-control" id="negotiationMessage" v-model="negotiationMessage"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" @click="submitNegotiation">Submit Negotiation</button>
        </div>
      </div>
    </div>
  </div>
</body>
</template>

<script>
import { Modal } from 'bootstrap';
export default {
  name: 'InfluencerDashboard',
  data() {
    return {
      profile: {
        ProfilePic: '',
        UserName: '',
        Email: '',
        Platforms: '',
        Niche: '',
        Followers: 0,
        Reach: 0,
        TotalEarning: 0,
        MonthlyEarning: 0,
        InfluencerID: null
      },
      averageRating: null,
      ratingCount: 0,
      isViewing: true,
      error: null,
      selectedFile: null,
      acceptedAds: [],
      pendingAds: [],
      recievedAds: [],
      negotiationModal: null,
      negotiationAmount: null,
      negotiationMessage: '',
      currentRequest: null
    };
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await fetch('http://127.0.0.1:5000/influencer/profile/update', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          const data = await response.json();
          if (data.ProfilePic) {
            data.ProfilePic = `http://127.0.0.1:5000${data.ProfilePic}`;
          }
          this.profile = data;
          await this.fetchAverageRating(); 
        } else {
          console.error('Failed to fetch profile');
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async updateProfile() {
      try {
        const formData = new FormData();
        formData.append('UserName', this.profile.UserName);
        formData.append('Email', this.profile.Email);
        formData.append('Platforms', this.profile.Platforms);
        formData.append('Niche', this.profile.Niche);
        formData.append('Followers', this.profile.Followers);
        formData.append('Reach', this.profile.Reach);
        formData.append('TotalEarning', this.profile.TotalEarning);
        formData.append('MonthlyEarning', this.profile.MonthlyEarning);
        if (this.selectedFile) {
          formData.append('ProfilePic', this.selectedFile);
        }

        const response = await fetch('http://127.0.0.1:5000/influencer/profile/update', {
          method: 'PUT',
          headers: {
            Authorization: 'Bearer ' + localStorage.getItem('token')
          },
          body: formData
        });
        if (response.ok) {
          this.isViewing = true; 
          this.fetchProfile(); 
        } else {
          console.error('Failed to update profile');
        }
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    toggleViewEdit() {
      this.isViewing = !this.isViewing;
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    async fetchAdsData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/requests', {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem('token')
          }
        });
        if (response.ok) {
          const requests = await response.json();
          this.acceptedAds = requests.filter(request => request.Status === 'Accepted');
          this.pendingAds = requests.filter(request => request.Status === 'Pending');
          this.recievedAds = requests.filter(request => request.Status === 'Pending' && request.ReceiverSponsorID === null);
        } else {
          console.error('Failed to fetch requests data');
        }
      } catch (error) {
        console.error('Error fetching requests data:', error);
      }
    },
    async takeAction(requestId, action) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/requests/${requestId}/${action}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem('token')
          }
        });

        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          await this.fetchAdsData(); 
        } else {
          console.error('Failed to perform action');
          alert('Failed to perform action. Please try again.');
        }
      } catch (error) {
        console.error('Error performing action:', error);
        alert('Error performing action. Please try again.');
      }
    },
    openNegotiationModal(request) {
      this.currentRequest = request;
      this.negotiationAmount = request.ProposedAmount; 
      this.negotiationMessage = ''; 
      this.negotiationModal.show(); 
    },
    async submitNegotiation() {
      if (!this.negotiationAmount || !this.currentRequest) {
        alert('Please specify an amount.');
        return;
      }

      const negotiationData = {
        amount: this.negotiationAmount,
        message: this.negotiationMessage
      };

      try {
        const response = await fetch(`http://127.0.0.1:5000/requests/negotiate/${this.currentRequest.RequestID}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem('token'),
          },
          body: JSON.stringify(negotiationData)
        });

        if (response.ok) {
          const data = await response.json();
          alert(data.message); 
          await this.fetchAdsData();
          this.negotiationModal.hide();
        } else {
          console.error('Failed to submit negotiation');
          alert('Failed to submit negotiation. Please try again.');
        }
      } catch (error) {
        console.error('Error submitting negotiation:', error);
        alert('Error submitting negotiation. Please try again.');
      }
    },
    async fetchAverageRating() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/average-rating/${this.profile.InfluencerID}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('token')
          }
        });

        if (response.ok) {
          const data = await response.json();
          this.averageRating = data.average_rating;
          this.ratingCount = data.rating_count;
        } else {
          console.error('Failed to fetch average rating');
        }
      } catch (error) {
        console.error('Error fetching average rating:', error);
      }
    }
  },
  mounted() {
    this.fetchProfile();
    this.fetchAdsData();
    this.negotiationModal = new Modal(document.getElementById('negotiationModal'));
  }
};
</script>

<style scoped>
    body {
      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      color: #ffffff;
      font-family: 'Arial', sans-serif;
    }
    .glass-effect {
      background: rgba(255, 255, 255, 0.1);
      backdrop-filter: blur(10px);
      border-radius: 15px;
      padding: 20px;
      margin-top: 20px;
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    .navbar {
      background: rgba(255, 255, 255, 0.1) !important;
      backdrop-filter: blur(10px);
    }
    .profile-pic {
      width: 150px;
      height: 150px;
      object-fit: cover;
      border: 4px solid #ffffff;
      box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }
    .glass-table {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(5px);
      border-radius: 10px;
      overflow: hidden;
    }
    .glass-table th {
      background: rgba(255, 255, 255, 0.1);
    }
    .btn-primary {
      background-color: #3a6ea5;
      border-color: #3a6ea5;
    }
    .btn-primary:hover {
      background-color: #2a5298;
      border-color: #2a5298;
    }
    .text-primary {
      color: #a8d0e6 !important;
    }
    h1, h2, h3 {
      color: #f0f8ff;
      margin-bottom: 20px;
      font-family:"Trebuchet MS", Helvetica, sans-serif;
    }
</style>
