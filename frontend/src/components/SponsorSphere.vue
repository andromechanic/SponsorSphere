<template>
  <body>
  <div class="landing-page">
    <header>
      <div class="logo-holder">
        <img
          src="../assets/SS logo.jpg"
          alt="SponsorSphere Logo"
          class="logo"
        />
      </div>
      <h1 style="font-family: Copperplate, Papyrus, fantasy;">Welcome to SponsorSphere</h1>
    </header>
    <main>
      <section class="hero">
        <h2>Uniting brands with powerful voices</h2>
        <p>Revolutionizing the way brands and influencers collaborate</p>
        <button class="cta-button">Get Started</button>
      </section>
      <section class="features">
        <div style="background-color: #2a5298;" class="feature" @click="redirectTo('influencer/register')">
          <h3 style="color: azure;">For Influencers</h3>
          <p style="color: azure;">Connect with brands that match your values</p>
        </div>
        <div style="background-color: #1185be;" class="feature" @click="redirectTo('sponsor/register')">
          <h3 style="color: azure;">For Sponsors</h3>
          <p style="color: azure;">Find the perfect influencers for your brand</p>
        </div>
      </section>
    </main>
    <footer>
      <p>© 2024 SponsorSphere. All rights reserved.</p>
    </footer>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <h2>Select Your Profile</h2>
        <button @click="redirectTo('sponsor/register')" class="modal-button">
          I am a Sponsor
        </button>
        <button @click="redirectTo('influencer/register')" class="modal-button">
          I am an Influencer
        </button>
      </div>
    </div>
  </div>
</body>
</template>

<script>
export default {
  name: "LandingPage",
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    redirectTo(route) {
      this.$router.push({ path: `/${route}` });
    },
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background-color: #bed8fa;
  font-family: "Open Sans", Arial, sans-serif;
}

.landing-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  animation: fadeIn 1s ease-in-out;
}

header {
  margin-bottom: 50px;
}

.logo-holder {
  margin-bottom: 15px;
}

.logo {
  max-width: 180px;
  animation: slideInDown 1s ease-in-out;
}

h1 {
  font-size: 2.8em;
  color: #333;
  margin-bottom: 10px;
}

.hero {
  background: linear-gradient(to bottom right, #007bff, #00aaff);
  color: white;
  padding: 50px 20px;
  border-radius: 10px;
  margin-bottom: 60px;
  animation: fadeInUp 1s ease-in-out;
}

h2 {
  font-size: 2.5em;
  margin-bottom: 20px;
  font-family: Garamond, serif;
}

p {
  font-size: 1.2em;
  margin-bottom: 30px;
  font-family: "Courier New", Courier, monospace;
}

.cta-button {
  background-color: #ffaa00;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1.2em;
  cursor: pointer;
  border-radius: 50px;
  transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}

.cta-button:hover {
  background-color: #ff8800;
  transform: scale(1.05);
}

.features {
  display: flex;
  justify-content: space-between;
  margin-bottom: 60px;
}

.feature {
  text-align: center;
  flex-basis: 45%;
  background-color: white;
  padding: 30px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  animation: fadeIn 1s ease-in-out;
  cursor: pointer;
}

.feature:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

h3 {
  font-size: 1.8em;
  color: #333;
  margin-bottom: 15px;
}

.feature p {
  font-size: 1.1em;
  color: #555;
}

footer {
  padding: 20px 0;
  background-color: #f1f1f1;
  color: #777;
  border-radius: 10px;
  margin-top: 40px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: white;
  padding: 30px 20px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease-in-out;
}

.modal h2 {
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
}

.modal-button {
  background-color: #007bff;
  color: rgb(178, 231, 253);
  border: none;
  padding: 10px 20px;
  margin: 10px;
  font-size: 1.1em;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}

.modal-button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInDown {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
