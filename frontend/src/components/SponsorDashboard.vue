<template>
  <body>
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="d-flex justify-content-between w-100">
          <span class="navbar-brand" style="font-family: Copperplate, Papyrus, fantasy;" >Sponsor Sphere</span> 
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Dashboard</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href='/sponsor/campaign'>Campaigns</a>
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

    <div class="container-fluid">
      <div class="content-wrapper">
        <div class="content-section ad-requests">
          <h3>Ad Requests</h3>
          <div v-if="adRequests.length > 0" class="table-responsive" style="border-radius: 20px;">
            <table class="table">
              <thead>
                <tr>
                  <th>Campaign</th>
                  <th>Advertisement</th>
                  <th>Requested By</th>
                  <th>Proposed Amount</th>
                  <th>Negotiated Amount</th>
                  <th>Negotiated By</th>
                  <th>Date Requested</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in adRequests" :key="request.RequestID">
                  <td>{{ request.Campaign }}</td>
                  <td>{{ request.Advertisement }}</td>
                  <td>{{ request.Influencer ? request.Influencer : 'You' }}</td>
                  <td>{{ request['Proposed Amount'] }}</td>
                  <td>{{ request['Negotiated Amount'] }}</td>
                  <td>{{ request.NegotiatedBy }}</td>
                  <td>{{ new Date(request['Date Requested']).toLocaleString() }}</td>
                  <td>{{ request.Status }}</td>
                  <td>
                    <button style="width: 75px;" @click="takeAction(request.RequestID, 'accept')" class="btn btn-success btn-sm mb-1"
                      :disabled="!canAcceptRequest(request)">
                      Accept
                    </button>
                    <button style="width: 75px;" @click="takeAction(request.RequestID, 'decline')" class="btn btn-danger btn-sm mb-1"
                      :disabled="request.Status !== 'Pending'">
                      Decline
                    </button>
                    <button  style="width: 75px;" @click="openNegotiationModal(request)" class="btn btn-warning btn-sm mb-1"
                      :disabled="request.Status !== 'Pending'">
                      Negotiate
                    </button>
                    <button  @click="openRatingModal(request)" class="btn btn-custom btn-sm" style="background-color:#1185be ; color: azure; width: 75px;"
                      :disabled="!['Accepted', 'Declined'].includes(request.Status)">
                      Rate
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No ad requests found.</p>
          </div>
        </div>

        <div class="content-section active-campaigns">
          <h3>Active Campaigns</h3>
          <div v-if="activeCampaigns.length > 0" class="table-responsive" style=" border-radius: 20px;">
            <table class="table" style="border-radius: 10px;">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Budget</th>
                  <th>Start Date</th>
                  <th>End Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="campaign in activeCampaigns" :key="campaign.CampaignID">
                  <td>{{ campaign.Title }}</td>
                  <td>{{ campaign.Budget }}</td>
                  <td>{{ formatDate(campaign.StartDate) }}</td>
                  <td>{{ formatDate(campaign.EndDate) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else>
            <p>No active campaigns found.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Negotiation Modal -->
    <div class="modal fade" id="negotiationModal" tabindex="-1" aria-labelledby="negotiationModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="negotiationModalLabel">Negotiate Request</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
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
            <button type="button" class="btn btn-custom" @click="submitNegotiation">Submit Negotiation</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Rating Modal -->
    <div class="modal fade" id="ratingModal" tabindex="-1" aria-labelledby="ratingModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="ratingModalLabel">Rate Influencer</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="rating" class="form-label">Rating</label>
              <select class="form-select" id="rating" v-model="ratingData.rating">
                <option value="1">1 - Poor</option>
                <option value="2">2 - Fair</option>
                <option value="3">3 - Good</option>
                <option value="4">4 - Very Good</option>
                <option value="5">5 - Excellent</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="comment" class="form-label">Comment</label>
              <textarea class="form-control" id="comment" v-model="ratingData.comment" rows="3"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-custom" @click="submitRating">Submit Rating</button>
          </div>
        </div>
      </div>
    </div>
  </body>
</template>

<script>
import { Modal } from 'bootstrap';
export default {
  data() {
    return {
      allcampaign: [],
      token: localStorage.getItem('jwt_token'),
      User: localStorage.getItem('auth'),
      SponsorID: localStorage.getItem('SponsorID'),
      activeCampaigns: [],
      pausedCampaigns: [],
      adRequests: [],
      negotiationModal: null,
      negotiationAmount: null,
      negotiationMessage: '',
      currentRequest: null,
      userData: null, // Initialize userData
      ratingModal: null,
      ratingData: {
        rating: null,
        comment: '',
        requestId: null,
        influencerId: null
      }
    };
  },
  methods: {
    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      };
      return new Date(dateString).toLocaleString('en-US', options);
    },
    canAcceptRequest(request) {
      if (request.Status !== 'Pending') {
        return false;
      }

      if (request.ReceiverSponsorID === null) {
        return request.NegotiatedBy === 'Influencer';
      }

      return (
        request['Negotiated Amount'] === null ||
        request.NegotiatedBy === 'Influencer'
      );
    },
    Logout() {
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('userData');
      this.$router.push('/');
    },
    getallcampaigns() {
      fetch('http://127.0.0.1:5000/campaign', {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.token,
          "UserAuth": this.User
        }
      })
        .then(resp => resp.json())
        .then(data => {
          this.allcampaign = Array.isArray(data) ? data : [];
          this.pausedCampaigns = this.allcampaign.filter(campaign => {
            return campaign.Status === "Paused";
          });
          this.activeCampaigns = this.allcampaign.filter(campaign => {
            return campaign.Status === "Active";
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    getAdRequests() {
      fetch('http://127.0.0.1:5000/requests', {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.token,
        }
      })
        .then(resp => resp.json())
        .then(data => {
          this.adRequests = data;
        })
        .catch(error => {
          console.error("Error fetching ad requests:", error);
        });
    },
    takeAction(requestId, action) {
      fetch(`http://127.0.0.1:5000/requests/${requestId}/${action}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.token,
          "UserAuth": this.User
        }
      })
        .then(resp => resp.json())
        .then(data => {
          alert(data.message);
          this.getAdRequests(); 
        })
        .catch(error => {
          console.log(error);
          alert('Failed to perform action. Please try again.');
        });
    },
    openNegotiationModal(request) {
      this.currentRequest = request;
      this.negotiationAmount = request.ProposedAmount; 
      this.negotiationMessage = ''; 
      this.negotiationModal.show(); 
    },
    submitNegotiation() {
      if (!this.negotiationAmount || !this.currentRequest) {
        alert('Please specify an amount.');
        return;
      }

      const negotiationData = {
        amount: this.negotiationAmount,
        message: this.negotiationMessage
      };
      fetch(`http://127.0.0.1:5000/requests/${this.currentRequest.RequestID}/negotiate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.token,
        },
        body: JSON.stringify(negotiationData)
      })
        .then(resp => resp.json())
        .then(data => {
          alert(data.message); 
          this.getAdRequests(); 
          this.negotiationModal.hide(); 
        })
        .catch(error => {
          console.log(error);
          alert('Failed to submit negotiation. Please try again.');
        });
    },
    checkUserData() {
      const userData = localStorage.getItem('userData');

      if (userData) {
        this.userData = JSON.parse(userData);
      } else {
        console.error('User data not found in localStorage');
        this.$router.push('/sponsor/login'); 
      }
    },
    openRatingModal(request) {
      console.log("Request object:", request);
      if (!['Accepted', 'Declined'].includes(request.Status)) {
        alert('You can only rate active or declined requests.');
        return;
      }
      this.currentRequest = request;

      const influencerId = request.ReceiverInfluencerID || request.SenderInfluencerID;

      if (!influencerId) {
        console.error('No valid InfluencerID found in the request');
        alert('Unable to determine the Influencer for this request. Rating cannot be submitted.');
        return;
      }

      this.ratingData = {
        rating: null,
        comment: '',
        requestId: request.RequestID,
        influencerId: influencerId
      };
      console.log("Rating data:", this.ratingData);
      this.ratingModal.show();
    },
    async submitRating() {
      if (!this.ratingData.rating) {
        alert('Please select a rating.');
        return;
      }

      if (!this.ratingData.influencerId) {
        alert('Unable to determine the Influencer for this request. Rating cannot be submitted.');
        return;
      }

      try {
        const response = await fetch('http://127.0.0.1:5000/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + this.token
          },
          body: JSON.stringify({
            Rating: this.ratingData.rating,
            Comment: this.ratingData.comment,
            InfluencerID: this.ratingData.influencerId
          })
        });

        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          this.ratingModal.hide();
          this.getAdRequests(); 
        } else {
          const errorData = await response.json();
          alert('Failed to submit rating: ' + (errorData.message || 'Please try again.'));
        }
      } catch (error) {
        console.error('Error submitting rating:', error);
        alert('An error occurred while submitting the rating. Please try again.');
      }
    }
  },
  created() {
    this.getallcampaigns();
    this.getAdRequests();
    this.checkUserData(); 
  },
  mounted() {
    this.negotiationModal = new Modal(document.getElementById('negotiationModal'));
    this.ratingModal = new Modal(document.getElementById('ratingModal'));
  }
};
</script>
<style scoped>
:root {
  --primary-color: #ff4036c5;
  --light-color: #f8f9fa;
  --dark-color: #343a40;
}

body {
  font-family: Arial, sans-serif;
  background-color: var(--light-color);
  margin: 0;
  padding: 0;
  background-color: #1185be;
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

.container-fluid {
  width: 100%; 
  padding: 0; 
  margin-top: 25px;
  margin-left: 10px;
}

.content-wrapper {
  display: flex;
  gap: 5px;
  width: 100%; 
  overflow: hidden; 
}

.content-section {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.ad-requests {
  flex: 0 0 70%; 
  margin-left: 0; 
  
}

.active-campaigns {
  flex: 0 0 26%; 
}

h3 {
  color: var(--primary-color);
  margin-top: 0;
  font-family: "Trebuchet MS", Helvetica, sans-serif;
}

.table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 10px;
}

.table th,
.table td {
  padding: 0.75rem;
  border-bottom: 1px solid #1185be;
  
}

.table th {
  background-color: #1185be;
  font-weight: bold;
  text-align: left;
}

.btn-custom {
  background-color: var(--primary-color);
  color: var(--light-color);
  border: none;
  padding: 0.375rem 0.75rem;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-custom:hover {
  background-color: #e60000;
}

@media (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
  }
}
</style>
