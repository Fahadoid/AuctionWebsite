import { createRouter, createWebHashHistory } from "vue-router";
import Listall from "@/routes/ListItems.vue";
import Showitem from "@/routes/ShowItem.vue";
import CreateItem from "@/routes/CreateItem.vue";
import showProfile from "@/routes/ShowProfile.vue";
import changeProfile from "@/routes/ChangeProfile.vue";
import changeItem from "@/routes/ChangeItem.vue";
import changeQuery from "@/routes/ChangeQuery.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Listall
  },
  {
    path: "/profile/:id(\\d+)",
    name: "change_Profile",
    component: changeProfile
  },
  {
    path: "/profile",
    name: "Profile",
    component: showProfile
  },
  {
    path: "/items/new",
    name: "Create Item",
    component: CreateItem
  },
  {
    path: "/items/:id(\\d+)",
    name: "Items",
    component: Showitem
  },
  {
    path: "/change_items/:id(\\d+)",
    name: "change_Items",
    component: changeItem
  },
  {
    path: "/items/:item_id(\d+)/queries/:query_id(\d+)",
    name: "change question",
    component: changeQuery
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
