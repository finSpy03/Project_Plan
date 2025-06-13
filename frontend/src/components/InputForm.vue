<template>
  <form @submit.prevent="submit" class="d-flex justify-content-center mb-4">
    <div class="input-group" style="max-width: 600px; width: 100%;">
      <input
        v-model="keyword"
        type="text"
        class="form-control"
        placeholder="Contoh: jakarta, air terjun, pantai"
        required
      />
      <button type="submit" class="btn btn-primary">Cari</button>
    </div>
  </form>
</template>

<script>
export default {
  data() {
    return { keyword: '' }
  },
  methods: {
    submit() {
      this.$emit('submit', this.keyword.trim())
    }
  }
}
</script>
