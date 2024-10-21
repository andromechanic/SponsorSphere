<template>
  <body>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
      <a class="navbar-brand" style="font-family: Copperplate, Papyrus, fantasy;" href="#">Sponsor Sphere</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/influencer/dashboard" class="nav-link">My Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/influencer/find" class="nav-link active">Find Ads</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
  
  <div class="container mt-4">
    <div class="glass-effect">
      <h1 class="text-center mb-4">Find Ads</h1>
      <div class="row mb-4">
        <div class="col-md-6 offset-md-3">
          <input 
            type="text" 
            class="form-control"
            v-model="searchQuery" 
            placeholder="Search by Sponsor Name, Medium, or Amount"
            @input="filterAds"
          >
        </div>
      </div>
      <div class="table-responsive">
        <table class="table table-striped table-bordered glass-table">
          <thead>
            <tr>
              <th>Sponsor Name</th>
              <th>Final Amount</th>
              <th>Description</th>
              <th>Medium</th>
              <th>Campaign Title</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ad in filteredAds" :key="ad.AdvertisementID">
              <td>{{ ad.SponsorName }}</td>
              <td>{{ ad.FinalAmount }}</td>
              <td>{{ ad.Description }}</td>
              <td>{{ ad.Medium }}</td>
              <td>{{ ad.CampaignTitle }}</td>
              <td>
                <button @click="openQuotationModal(ad)" class="btn btn-primary btn-sm">Request Quotation</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quotation Modal -->
    <div class="modal fade" id="quotationModal" tabindex="-1" aria-labelledby="quotationModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="quotationModalLabel">Request Quotation</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="quotationAmount" class="form-label">Specify Amount</label>
              <input type="number" class="form-control" id="quotationAmount" v-model="quotationAmount">
            </div>
            <div class="mb-3">
              <label for="quotationMessage" class="form-label">Message (Optional)</label>
              <textarea class="form-control" id="quotationMessage" v-model="quotationMessage"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="submitQuotation">Submit Quotation</button>
          </div>
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
      ads: [],
      filteredAds: [],
      searchQuery: '',
      token: localStorage.getItem('token'),
      quotationModal: null,
      quotationAmount: null,
      quotationMessage: '',
      currentAd: null,
    };
  },
  mounted() {
    this.fetchAds();
    this.quotationModal = new Modal(document.getElementById('quotationModal'));
  },
  methods: {
    async fetchAds() {
      const url = 'http://127.0.0.1:5000/influencer/ads';
      const options = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.token,
        }
      };
      this.ads = await this.fetchData(url, options);
      this.filteredAds = [...this.ads];
    },
    
    async fetchData(url, options) {
      const response = await fetch(url, options);
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Error fetching data:', response.statusText, errorText);
        return [];
      }
      return await response.json();
    },

    filterAds() {
      const query = this.searchQuery.toLowerCase();
      this.filteredAds = this.ads.filter(ad => 
        ad.SponsorName.toLowerCase().includes(query) || 
        ad.Medium.toLowerCase().includes(query) ||
        ad.FinalAmount.toString().includes(query) 
      );
    },

    openQuotationModal(ad) {
      this.currentAd = ad;
      this.quotationAmount = null;
      this.quotationMessage = '';
      this.quotationModal.show();
    },

    async submitQuotation() {
      if (!this.quotationAmount || !this.currentAd) {
        alert('Please specify an amount.');
        return;
      }

      const url = 'http://127.0.0.1:5000/requests';
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.token,
        },
        body: JSON.stringify({
          amount: this.quotationAmount,
          ad_id: this.currentAd.AdvertisementID,
          campaign_id: this.currentAd.CampaignID,
          message: this.quotationMessage
        })
      };

      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          throw new Error('Failed to submit quotation');
        }
        const result = await response.json();
        alert(result.message);
        this.quotationModal.hide();
      } catch (error) {
        console.error('Error submitting quotation:', error);
        alert('Failed to submit quotation. Please try again.');
      }
    },

    logout() {
      localStorage.removeItem('token'); 
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
body {
      height: 100vh;
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
    h1 {
      color: #f0f8ff;
      margin-bottom: 20px;
      font-family: "Trebuchet MS", Helvetica, sans-serif;
    }
    .form-control {
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #ffffff;
    }
    .form-control::placeholder {
      color: rgba(255, 255, 255, 0.7);
    }
    .modal-content {
      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      color: #ffffff;
    }
    .modal-header, .modal-footer {
      border-color: rgba(255, 255, 255, 0.1);
    }
</style>
