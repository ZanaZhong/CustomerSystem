<script>
import axios from "axios";

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
        const response = await axios.get("http://localhost:8888/customers");
        this.customers = response.data;
      } catch (error) {
        console.error("無法取得客戶資料", error);
      }
    },
  },
};
</script>