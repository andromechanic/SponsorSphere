<template>
    <body>
        <div class="col-md-8 offset-md-2">
            <nav class="navbar navbar-expand-lg navbar-dark">
                <div class="d-flex justify-content-between w-100">
                    <span class="navbar-brand" style="font-family: Copperplate, Papyrus, fantasy;" >Sponsor Sphere</span>
                    <ul class="nav nav-tabs">
                        <li class="nav-item">
                            <a class="nav-link" aria-current="page" href="/sponsor/dashboard">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href='/sponsor/campaign'>Campaigns</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" href="/sponsor/find">Find</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" @click="Logout">Logout</a>
                        </li>
                    </ul>
                </div>
            </nav>

            <div class="card search-bar-card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Search Influencers</h5>
                    <input type="text" v-model="searchQuery" class="form-control" placeholder="Search by name or niche" />
                </div>
            </div>

            <div class="card influencer-list-card">
                <div class="card-body">
                    <div v-for="influencer in filteredInfluencers" :key="influencer.InfluencerID" class="influencer-item mb-3">
                        <div class="influencer-card">
                            <img :src="influencer.ProfilePic ? influencer.ProfilePic : require('@/assets/noprofile.jpg')"
                                alt="Profile Picture" class="influencer-image">
                            <p><strong>{{ influencer.UserName }}</strong></p>
                            <p>Niche: {{ influencer.Niche }}</p>
                            <p>Followers: {{ influencer.Followers }}</p>
                            <p>Platform: {{ influencer.Platforms }}</p>
                            <div>
                                <select v-model="selectedCampaign[influencer.InfluencerID]" class="form-control"
                                    @change="fetchAds(influencer.InfluencerID)">
                                    <option value="" disabled>Select a campaign</option>
                                    <option v-for="campaign in campaigns" :key="campaign.CampaignID" :value="campaign.CampaignID">
                                        {{ campaign.Title }}
                                    </option>
                                </select>
                            </div>
                            <div v-if="ads[influencer.InfluencerID] && ads[influencer.InfluencerID].length > 0">
                                <select v-model="selectedAd[influencer.InfluencerID]" class="form-control">
                                    <option value="" disabled>Select an ad</option>
                                    <option v-for="ad in ads[influencer.InfluencerID]" :key="ad.AdvertisementID"
                                        :value="ad.AdvertisementID">
                                        {{ ad.Description }}
                                    </option>
                                </select>
                            </div>
                            <div>
                                <label>Request Amount:</label>
                                <input type="number" v-model="requestAmount[influencer.InfluencerID]" class="form-control"
                                    placeholder="Enter amount">
                            </div>
                            <button class="btn btn-primary mt-2" @click="requestAd(influencer.InfluencerID)">Request Ad</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
</template>

<script>
export default {
    data() {
        return {
            influencers: [],
            campaigns: [],
            searchQuery: '',
            selectedCampaign: {},
            requestAmount: {},
            token: localStorage.getItem('jwt_token'),
            userData: JSON.parse(localStorage.getItem('userData')),
            ads: {},
            selectedAd: {},
            feedback: {},
        };
    },
    computed: {
        filteredInfluencers() {
            return this.influencers.filter((influencer) => {
                return influencer.UserName.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    influencer.Niche.toLowerCase().includes(this.searchQuery.toLowerCase());
            });
        }
    },
    created() {
        this.fetchInfluencers();
        this.getAllCampaigns();
        this.refreshUserData();
    },
    methods: {
        async fetchInfluencers() {
            try {
                const response = await fetch('http://127.0.0.1:5000/influencer/profile', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: 'Bearer ' + this.token,
                    }
                });
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                
                this.influencers = data.map(influencer => {
                    if (influencer.ProfilePic) {
                        influencer.ProfilePic = `http://127.0.0.1:5000${influencer.ProfilePic}`;
                    }
                    this.feedback[influencer.InfluencerID] = { Rating: '', Comment: '' };
                    return influencer;
                });
            } catch (error) {
                console.error('Failed to fetch influencers:', error);
            }
        },

        async getAllCampaigns() {
            try {
                const response = await fetch("http://127.0.0.1:5000/campaign", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + this.token,
                        UserAuth: JSON.stringify(this.userData),
                    },
                });
                if (!response.ok) {
                    throw new Error(`Error fetching campaigns: ${response.status}`);
                }
                const data = await response.json();
                this.campaigns = Array.isArray(data) ? data.filter(campaign => campaign.Status === 'Active') : [];
            } catch (error) {
                console.error("Error fetching campaigns:", error);
            }
        },

        async fetchAds(influencerID) {
            const selectedCampaignID = this.selectedCampaign[influencerID];
            if (!selectedCampaignID) return;

            try {
                const response = await fetch(`http://127.0.0.1:5000/campaign/${selectedCampaignID}/ads`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: 'Bearer ' + this.token,
                    }
                });
                if (!response.ok) {
                    throw new Error(`Error fetching ads: ${response.status}`);
                }
                this.ads[influencerID] = await response.json();
            } catch (error) {
                console.error('Error fetching ads:', error);
            }
        },

        async requestAd(influencerID) {
            const selectedCampaignID = this.selectedCampaign[influencerID];
            const selectedAdID = this.selectedAd[influencerID];
            const amount = this.requestAmount[influencerID];

            console.log("Selected Campaign ID:", selectedCampaignID);
            console.log("Selected Ad ID:", selectedAdID);
            console.log("Requested Amount:", amount);
            console.log("Influencer ID:", influencerID);

            if (!selectedCampaignID || !selectedAdID || !amount) {
                alert("Please select a campaign, an ad, and enter an amount.");
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:5000/requests/sponsor/to_influencer/${influencerID}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: 'Bearer ' + this.token,
                    },
                    body: JSON.stringify({
                        amount: amount,
                        ad_id: selectedAdID,
                        campaign_id: selectedCampaignID
                    })
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log('Request sent successfully:', result);
                    alert("Ad request sent successfully!");
                } else {
                    console.error('Failed to send request:', response.statusText);
                    alert("Failed to send request. Please try again.");
                }
            } catch (error) {
                console.error('Error occurred:', error);
                alert("An error occurred while sending the request. Please try again.");
            }
        },

        goBackToCampaigns() {
            this.$router.push('/sponsor/campaign');
        },

        Logout() {
            localStorage.removeItem('jwt_token');
            localStorage.removeItem('userData');
            this.userData = null;
            this.$router.push('/');
        },
        refreshUserData() {
            const storedUserData = localStorage.getItem('userData');
            if (storedUserData) {
                this.userData = JSON.parse(storedUserData);
            } else {
                console.error('User data not found in localStorage');
            }
        }
    }
};
</script>

<style scoped>
body {
    font-family: Arial, sans-serif;
    background-color: #1185be;
}

.card {
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    background-color: rgba(255, 255, 255, 0.8);
}

.search-bar-card {
    margin-bottom: 20px;
}

.influencer-item {
    margin-bottom: 15px;
}

.influencer-card {
    background: rgba(255, 255, 255, 0.7); 
  backdrop-filter: blur(1px);
  border-radius: 10px; 
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); 
  padding: 20px; 
  border: 1px solid rgba(255, 255, 255, 0.2); 
}

.influencer-image {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin-bottom: 10px;
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
