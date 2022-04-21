import axios, {AxiosInstance} from "axios";
import {authStore} from "./stores";
import {Token} from "./types/api/token";

const axiosAPI: AxiosInstance = axios.create({
  baseURL: process.env.API_URL
});

let token = <Token>{};
authStore.subscribe((value) => (token=value))

const apiRequest = (method, url: string, data?: any) => {
  const headers = {
    authorization: "Bearer " + token.access_token,
    "Content-type": "application/json",
  };

  return axiosAPI({
    method,
    url,
    data: data,
    headers
  }).then(res => {
    return Promise.resolve(res.data);
  })
  .catch(err => {
    if (err.response.status === 401) {
      console.log(err.response.status + ' re-directing to /auth/github');
      window.location.href = '/auth/github';
    }
    return Promise.reject(err);
  });
};

const get = (url) => apiRequest("get", url);

const deleteRequest = (url) => apiRequest("delete", url);

const post = (url, data) => apiRequest("post", url, data);

const put = (url, data) => apiRequest("put", url, data);


const API = {
  get,
  delete: deleteRequest,
  post,
  put,
};

export default API;
