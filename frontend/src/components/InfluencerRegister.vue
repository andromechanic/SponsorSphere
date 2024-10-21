<template>
  <div class="card-container">
    <div :class="['card', { 'card-flip': isFlipped }]">
      <div class="card-face card-face-front">
        <h1>Influencer Sign In</h1>
        <form @submit.prevent="signIn" class="form">
          <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required />
          </div>
          <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required />
          </div>
          <button type="submit" class="btn">Sign In</button>
        </form>
        <button @click="flipCard" class="btn">Register as an Influencer</button>
        <div v-if="error" class="error-message">{{ error }}</div>
      </div>

      <div class="card-face card-face-back">
        <h2>Influencer Registration</h2>
        <form @submit.prevent="register" class="form">
          <div class="form-group">
            <label for="UserName">Username:</label>
            <input
              type="text"
              id="UserName"
              v-model="UserName"
              placeholder="Enter your username"
              required
            />
          </div>
          <div class="form-group">
            <label for="Email">Email:</label>
            <input
              type="email"
              id="Email"
              v-model="Email"
              placeholder="Enter your email"
              required
            />
          </div>
          <div class="form-group">
            <label for="Password">Password:</label>
            <input
              type="password"
              id="Password"
              v-model="Password"
              placeholder="Enter your password"
              required
            />
          </div>
          <div class="form-group">
            <label for="Platforms">Platforms:</label>
            <input
              type="text"
              id="Platforms"
              v-model="Platforms"
              placeholder="Enter the platforms you use"
              required
            />
          </div>
          <div class="form-group">
            <label for="Niche">Niche:</label>
            <input
              type="text"
              id="Niche"
              v-model="Niche"
              placeholder="Enter your niche"
              required
            />
          </div>
          <button type="submit" class="btn">Register</button>
        </form>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>
        <button @click="flipCard" class="btn">Back to Sign In</button>
      </div>
    </div>
    <div class="nav-buttons">
      <button @click="navigateToSponsorLogin" class="btn nav-btn">
        Sponsor Login
      </button>
      <button @click="navigateToAdminLogin" class="btn nav-btn">
        Admin Login
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      UserName: "",
      Email: "",
      Password: "",
      Platforms: "",
      Niche: "",
      error: null,
      success: null,
      isFlipped: false,
    };
  },
  methods: {
    async signIn() {
      try {
        this.error = null;
        const response = await fetch("http://127.0.0.1:5000/influencer/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            UserName: this.username,
            Password: this.password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem("token", data.token);
          this.$router.push("/influencer/dashboard");
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Login failed.";
        }
      } catch (err) {
        this.error = "An error occurred: " + err.message;
      }
    },
    async register() {
      try {
        this.error = null;
        this.success = null;

        if (
          !this.UserName ||
          !this.Email ||
          !this.Password ||
          !this.Platforms ||
          !this.Niche
        ) {
          this.error = "Please fill in all fields.";
          return;
        }

        const response = await fetch(
          "http://127.0.0.1:5000/influencer/signup",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              UserName: this.UserName,
              Email: this.Email,
              Password: this.Password,
              Platforms: this.Platforms,
              Niche: this.Niche,
            }),
          }
        );

        if (response.status === 409) {
          this.error = "Username or Email already exists";
        } else if (response.status === 201) {
          const data = await response.json();
          this.success = data.message || "Registration successful!";
          this.UserName = "";
          this.Email = "";
          this.Password = "";
          this.Platforms = "";
          this.Niche = "";
        } else {
          const data = await response.json();
          this.error = data.message || "An error occurred during registration.";
        }
      } catch (err) {
        this.error = "An error occurred: " + err.message;
      }
    },
    flipCard() {
      this.isFlipped = !this.isFlipped;
    },
    navigateToSponsorLogin() {
      this.$router.push("/sponsor/register");
    },
    navigateToAdminLogin() {
      this.$router.push("/admin/signin");
    },
  },
};
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box;
}

body {
  background: linear-gradient(to right, #b8caf5, #ffffff);
}
</style>
<style scoped>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  width: 100%;
  box-sizing: border-box;
}
.card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100%;
  padding: 0px;
  overflow: hidden;
  position: relative;
  background: linear-gradient(to right, #afdbff, #ffffff);
}

.nav-btn {
  margin-bottom: 10px;
  padding: 10px 20px;
  background-color: #ffffff;
  border: 2px solid #b74b4b;
  color: #b74b4b;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background-color: #b74b4b;
  color: #ffffff;
}
.card {
  position: relative;
  width: 100%;
  max-width: 600px;
  min-height: 700px;
  perspective: 1200px;
  transition: transform 0.6s ease;
}

.card-face {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 15px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.9);
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  transition: transform 0.6s ease, width 0.6s ease, height 0.6s ease;
}

.card-face h1,
.card-face h2 {
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
  text-align: center;
}

.form {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background-color: #f1f1f1;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.form-group input:focus {
  outline: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  color: #fff;
  background-color: #4b86b7;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease,
    box-shadow 0.3s ease;
  font-size: 16px;
  margin-top: 10px;
}

.btn:hover {
  background-color: #0055ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.nav-buttons {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
}

.nav-btn {
  margin-bottom: 10px;
  padding: 10px 20px;
  background-color: #ffffff;
  border: 2px solid #544bb7;
  color: #4b6fb7;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.error-message,
.success-message {
  background-color: #dc3545;
  color: #fff;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
}

.success-message {
  background-color: #28a745;
}

.card-face-front {
  transform: rotateY(0deg);
}

.card-face-back {
  transform: rotateY(180deg);
}

.card-flip .card-face-front {
  transform: rotateY(180deg);
  width: 100%;
  height: 100%;
}

.card-flip .card-face-back {
  transform: rotateY(0deg);
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .card {
    min-height: 400px;
  }

  .card-face h1,
  .card-face h2 {
    font-size: 20px;
  }

  .form-group input,
  .btn {
    padding: 10px;
  }

  .nav-btn {
    width: 160px;
  }
}
</style>
