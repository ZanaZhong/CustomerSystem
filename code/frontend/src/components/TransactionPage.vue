<template>
  <div class="container mt-4">
    <h1 class="text-center mb-4">客戶資料</h1>

    <!-- 交易紀錄查詢表單 -->
    <h2 class="mb-3">查詢客戶交易紀錄</h2>
    <form @submit.prevent="fetchCustomerTransactions" class="card">
      <div class="form-row">
        <div class="col">
          <label for="customerSelect" class="form-label">選擇客戶</label>
          <select v-model="selectedCustomerId" id="customerSelect" class="form-control" required>
            <option v-for="customer in customers" :key="customer.id" :value="customer.id">
              {{ customer.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-row mt-3">
        <div class="col">
          <label for="startDate" class="form-label">開始日期</label>
          <input type="date" id="startDate" v-model="startDate" class="form-control" required />
        </div>
        ~
        <div class="col">
          <label for="endDate" class="form-label">結束日期</label>
          <input type="date" id="endDate" v-model="endDate" class="form-control" required />
        </div>
      </div>

      <button type="submit" class="btn btn-primary btn-block mt-4">查詢交易紀錄</button>
    </form>

    <!-- 顯示交易紀錄 -->
    <div v-if="transactions.length > 0" class="mt-4">
      <h3>交易紀錄</h3>
      <table class="table table-bordered table-striped customer-table" >
        <thead>
          <tr>
            <th>客戶ID</th>
            <th>交易日期</th>
            <th>金額</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="transaction in transactions" :key="transaction.id">
            <td>{{ transaction.id }}</td>
            <td>{{ transaction.date }}</td>
            <td>{{ transaction.amount }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="mt-3 text-center">尚未查詢到交易紀錄</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      customers: [],
      selectedCustomerId: null,
      startDate: '',
      endDate: '',
      transactions: [],
    };
  },
  mounted() {
    this.fetchCustomersName();
  },
  methods: {
    // fetch all customers' names
    async fetchCustomersName() {
      try {
        const response = await axios.get('http://localhost:8888/customer_names');
        this.customers = response.data;
      } catch (error) {
        console.error('無法取得客戶資料', error);
      }
    },

    // search customer's transactions by time range
    async fetchCustomerTransactions() {
      try {
        const response = await axios.get(`http://localhost:8888/transactions/${this.selectedCustomerId}`, {
          params: {
            startDate: this.startDate,
            endDate: this.endDate,
          },
        });
        this.transactions = response.data;
      } catch (error) {
        alert(`查詢失敗: ${error.response?.data?.error || '伺服器錯誤'}`);
        console.error('查詢交易紀錄失敗', error);
      }
    },
  },
};
</script>

<style scoped>
.card {
  max-width: 600px;
  margin: auto;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-row input,
.form-row select,
.form-row button {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc; /* 預設邊框 */
  border-radius: 0.25rem; /* 圓角邊框 */
}

/* 表單欄位的間距以及對齊 */
.form-row label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-control {
  border-radius: 4px;
}

.btn-block {
  width: 100%;
}

.table th {
  background-color: #f8f9fa;
}

.table-bordered {
  border: 1px solid #dee2e6;
}

.table th, .table td {
  text-align: center;
}

.customer-table th,
.customer-table td {
  padding: 10px 15px;
  border: 1px solid #ddd;
  text-align: center;
}

.customer-table th {
  background-color: #2c3e50;
  color: #ffffff;
}

.customer-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.customer-table tr:hover {
  background-color: #f1f1f1;
}

/* 響應式 */
@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  .card {
    margin-top: 20px;
  }

  .form-row {
    display: block; /* 小螢幕下讓表單欄位顯示為垂直 */
  }

  .col {
    margin-bottom: 10px; /* 小螢幕下每個欄位有一些底部間距 */
  }
}

.mt-3 {
  margin-top: 1rem !important;
}

.mt-4 {
  margin-top: 1.5rem !important;
}

</style>



