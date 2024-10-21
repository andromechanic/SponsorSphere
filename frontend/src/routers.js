import { createRouter, createWebHistory } from "vue-router";
import SponsorRegister from "@/components/SponsorRegister";
import InfluencerRegister from "@/components/InfluencerRegister";
import AdminSignIn from "@/components/AdminSignIn";
import SponsorDashboard from "@/components/SponsorDashboard";
import SponsorSphere from "@/components/SponsorSphere.vue";
import CampaignDashboard from "./components/CampaignDashboard.vue";
import SponsorFind from "./components/SponsorFind.vue";
import ViewAds from "./components/ViewAds.vue";
import InfluencerDashboard from "./components/InfluencerDashboard.vue";
import InfluencerFind from "./components/InfluencerFind.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import AdminFind from "./components/AdminFind.vue"
import AdminStats from "./components/AdminStats.vue";

const routes = [
  {
    path: "/",
    name: "SponsorSphere",
    component: SponsorSphere,
  },
  {
    path: "/sponsor/register",
    name: "SponsorRegister",
    component: SponsorRegister,
  },
  {
    path: "/sponsor/dashboard",
    name: "SponsorDashboard",
    component: SponsorDashboard,
  },
  {
    path: "/sponsor/campaign",
    name: "CampaignDashboard",
    component: CampaignDashboard,
  },
  {
    path: '/viewads/:campaignId',
    name: 'ViewAds',
    component: ViewAds,
  },

  {
    path: "/sponsor/find",
    name: "SponsorFind",
    component: SponsorFind,
  },
  {
    path: "/influencer/register",
    name: "InfluencerRegister",
    component: InfluencerRegister,
  },
  {
    path: "/influencer/dashboard",
    name: "InfluencerDashboard",
    component: InfluencerDashboard,
  },
  {
    path: '/influencer/find',
    name: 'InfluencerFind',
    component: InfluencerFind,
  },
  {
    path: "/admin/signin",
    name: "AdminSignIn",
    component: AdminSignIn,
  },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
  },
  {
    path: "/admin/find",
    name: "AdminFind",
    component: AdminFind,
  },
  {
    path: "/admin/stats",
    name: "AdminStats",
    component: AdminStats,
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
