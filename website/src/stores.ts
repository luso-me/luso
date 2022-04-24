import {writable} from "svelte/store";
import type {Token} from "./types/api/token";
import {UserInfo} from "./types/api/user";

const localAuthStore = localStorage.getItem("luso-store-auth");
export const authStore = writable<Token>(JSON.parse(localAuthStore) || {});
authStore.subscribe(value => localStorage.setItem("luso-store-auth", JSON.stringify(value)));

const localUserInfoStore = localStorage.getItem("luso-store-user-info");
export const userInfoStore = writable<UserInfo>(JSON.parse(localUserInfoStore) || {});
userInfoStore.subscribe(value => localStorage.setItem("luso-store-user-info", JSON.stringify(value)));
