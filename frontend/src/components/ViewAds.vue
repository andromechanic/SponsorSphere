<template>

    <body>
        <div class="view-ads-container">
            <div class="header">
                <h1 style="font-family: Trebuchet MS, Helvetica, sans-serif;">Your Advertisements</h1>
                <button @click="goBack" class="btn btn-secondary">Back to Campaigns</button>
            </div>

            <div class="row">
                <div class="col-md-6">
                    <div class="card ad-form-card">
                        <div class="card-body">
                            <h3 style="font-family: Trebuchet MS, Helvetica, sans-serif;" class="card-title">{{ isEditing ? 'Edit Advertisement' : 'Add New Advertisement' }}</h3>
                            <form @submit.prevent="submitAd">
                                <div class="form-group">
                                    <label for="description" class="form-label">Description</label>
                                    <input type="text" class="form-control" id="description" v-model="newAd.Description"
                                        required />
                                </div>
                                <div class="form-group">
                                    <label for="amount" class="form-label">Amount</label>
                                    <input type="number" class="form-control" id="amount" v-model="newAd.Amount"
                                        required />
                                </div>
                                <div class="form-group">
                                    <label for="finalAmount" class="form-label">Final Amount</label>
                                    <input type="number" class="form-control" id="finalAmount"
                                        v-model="newAd.FinalAmount" required />
                                </div>
                                <div class="form-group">
                                    <label for="medium" class="form-label">Medium</label>
                                    <input type="text" class="form-control" id="medium" v-model="newAd.Medium"
                                        required />
                                </div>
                                <button type="submit" style="margin-top: 18px;" class="btn btn-primary">{{ isEditing ? 'Update Advertisement' :
                                    'Add Advertisement' }}</button>
                                <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
                            </form>
                        </div>
                    </div>
                </div>

                <div class="col-md-6">
                    <div class="card ads-list-card">
                        <div class="card-body">
                            <h3 style="font-family: Trebuchet MS, Helvetica, sans-serif;" class="card-title">Advertisements List</h3>
                            <table class="table" v-if="ads.length">
                                <thead>
                                    <tr>
                                        <th>Description</th>
                                        <th>Amount</th>
                                        <th>Final Amount</th>
                                        <th>Medium</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="ad in ads" :key="ad.AdvertisementID">
                                        <td>{{ ad.Description }}</td>
                                        <td>{{ ad.Amount }}</td>
                                        <td>{{ ad.FinalAmount }}</td>
                                        <td>{{ ad.Medium }}</td>
                                        <td>
                                            <button @click="editAd(ad)" class="btn btn-warning">Edit</button>
                                            <button @click="deleteAd(ad.AdvertisementID)"
                                                class="btn btn-danger">Delete</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <p v-else>No advertisements found for this campaign.</p>
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
            ads: [],
            newAd: {
                Description: '',
                Amount: 0,
                FinalAmount: 0,
                Medium: ''
            },
            selectedCampaign: null,
            token: localStorage.getItem("jwt_token"),
            User: localStorage.getItem("auth"),
            isEditing: false,
            editingAdId: null,
            campaignBudget: 0,
            errorMessage: ''
        };
    },
    mounted() {
        this.selectedCampaign = this.$route.params.campaignId;
        this.fetchAds();
        this.fetchCampaignBudget();
    },
    methods: {
        goBack() {
            this.$router.push('/sponsor/campaign');
        },
        fetchAds() {
            if (!this.selectedCampaign) return;
            fetch(`http://127.0.0.1:5000/campaign/${this.selectedCampaign}/ads`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + this.token,
                    "UserAuth": this.User,
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.ads = Array.isArray(data) ? data : [];
                })
                .catch(error => {
                    console.error('Error fetching ads:', error);
                });
        },
        fetchCampaignBudget() {
            fetch(`http://127.0.0.1:5000/campaign/${this.selectedCampaign}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + this.token,
                    "UserAuth": this.User,
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.campaignBudget = data.Budget;
                })
                .catch(error => {
                    console.error('Error fetching campaign budget:', error);
                });
        },
        submitAd() {
            if (this.isEditing) {
                this.updateAd();
            } else {
                this.addAd();
            }
        },
        addAd() {
            if (this.totalFinalAmount() + this.newAd.FinalAmount > this.campaignBudget) {
                this.errorMessage = 'Total final amounts exceed the campaign budget.';
                return;
            }
            fetch(`http://127.0.0.1:5000/advertisement`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + this.token,
                    "UserAuth": this.User,
                },
                body: JSON.stringify({
                    Amount: this.newAd.Amount,
                    FinalAmount: this.newAd.FinalAmount,
                    Description: this.newAd.Description,
                    Medium: this.newAd.Medium,
                    CampaignID: this.selectedCampaign
                })
            })
                .then(response => response.json())
                .then(data => {
                    this.ads.push(data);
                    this.resetForm();
                })
                .catch(error => {
                    console.error('Error adding ad:', error);
                });
        },
        editAd(ad) {
            this.isEditing = true;
            this.editingAdId = ad.AdvertisementID;
            this.newAd = { ...ad };
        },
        updateAd() {
            if (this.totalFinalAmount() - this.ads.find(ad => ad.AdvertisementID === this.editingAdId).FinalAmount + this.newAd.FinalAmount > this.campaignBudget) {
                this.errorMessage = 'Total final amounts exceed the campaign budget.';
                return;
            }
            fetch(`http://127.0.0.1:5000/advertisement/${this.editingAdId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + this.token,
                    "UserAuth": this.User,
                },
                body: JSON.stringify({
                    Amount: this.newAd.Amount,
                    FinalAmount: this.newAd.FinalAmount,
                    Description: this.newAd.Description,
                    Medium: this.newAd.Medium,
                    CampaignID: this.selectedCampaign
                })
            })
                .then(response => {
                    if (response.ok) {
                        const index = this.ads.findIndex(ad => ad.AdvertisementID === this.editingAdId);
                        this.ads[index] = { ...this.newAd, AdvertisementID: this.editingAdId };
                        this.resetForm();
                    }
                })
                .catch(error => {
                    console.error('Error updating ad:', error);
                });
        },
        deleteAd(advertisementId) {
            fetch(`http://127.0.0.1:5000/advertisement/${advertisementId}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + this.token,
                    "UserAuth": this.User,
                }
            })
                .then(response => {
                    if (response.ok) {
                        this.ads = this.ads.filter(ad => ad.AdvertisementID !== advertisementId);
                    }
                })
                .catch(error => {
                    console.error('Error deleting ad:', error);
                });
        },
        totalFinalAmount() {
            return this.ads.reduce((total, ad) => total + ad.FinalAmount, 0);
        },
        resetForm() {
            this.newAd = { Description: '', Amount: 0, FinalAmount: 0, Medium: '' };
            this.isEditing = false;
            this.editingAdId = null;
            this.errorMessage = '';
        }
    }
}
</script>

<style scoped>
body {
    font-family: Arial, sans-serif;
    background-color: #1185be;
    margin: 0;
    padding: 0;
    background-color: #1185be;
    height: 100vh;
}
.table th,
.table td {
  color: rgb(0, 0, 0); 
}

.table th {
  background-color: #1185be; 
  color: white;
}

.view-ads-container {
    padding: 20px;
    background: rgba(255, 255, 255, 0.7);
    background-color: #1185be;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.row {
    margin-top: 20px;
}

.ad-form-card,
.ads-list-card {
    margin-bottom: 20px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(1px);
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-title {
    margin-bottom: 15px;
}
</style>
