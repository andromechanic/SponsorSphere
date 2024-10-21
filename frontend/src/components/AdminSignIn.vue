<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="login-title">Admin Sign In</h1>
      <form class="login-form" @submit.prevent="signIn">
        <div class="input-group">
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit" class="login-btn">Sign In</button>
      </form>
    </div>
    <div class="nav-buttons">
      <button @click="navigateToInfluencerLogin" class="nav-btn">
        Influencer Login
      </button>
      <button @click="navigateToSponsorLogin" class="nav-btn">
        Sponsor Login
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
      error: null,
    };
  },
  methods: {
    async signIn() {
      try {
        this.error = null; 

        if (!this.username || !this.password) {
          this.error = "Please fill in both fields.";
          return;
        }

        const response = await fetch("http://127.0.0.1:5000/admin/login", {
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
          this.$router.push("/admin/dashboard"); 
        } else {
          const errorData = await response.json();
          this.error = errorData.message || "Login failed.";
        }
      } catch (err) {
        this.error = "An error occurred: " + err.message;
      }
    },
    navigateToInfluencerLogin() {
      this.$router.push("/influencer/register");
    },
    navigateToSponsorLogin() {
      this.$router.push("/sponsor/register");
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #1f4037, #99f2c8);
  position: relative;
}

.login-box {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
  transition: transform 0.3s ease-in-out;
}

.login-box:hover {
  transform: translateY(-10px);
}

.login-title {
  margin-bottom: 30px;
  font-size: 28px;
  color: #1f4037;
  font-weight: 600;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.input-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.input-group input:focus {
  border-color: #1f4037;
  outline: none;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #1f4037;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.login-btn:hover {
  background-color: #99f2c8;
  color: #1f4037;
  transform: translateY(-3px);
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-buttons {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
}

.nav-btn {
  display: block;
  width: auto;
  padding: 12px;
  background-color: #ffffff;
  border: 1px solid #1f4037;
  color: #1f4037;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
  margin-bottom: 10px;
}

.nav-btn:hover {
  background-color: #1f4037;
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
