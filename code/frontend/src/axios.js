// import axios from 'axios';

// const axiosInstance = axios.create({
//   baseURL: 'http://localhost:8888', // Flask 後端 URL
// });

// export default axiosInstance;





import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8888'; // Base URL for the API

export default {
  data() {
    return {
      customers: [],
    };
  },
  mounted() {
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      try {
        const response = await axios.get("/customers");
        this.customers = response.data;
      } catch (error) {
        console.error("無法取得客戶資料", error);
      }
    },
  },
};
