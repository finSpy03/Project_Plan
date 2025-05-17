<template>
  <div class="flex gap-2 mb-6">
    <input
      v-model="keyword"
      placeholder="Masukkan Kota, contoh: Jakarta"
      class="flex-1 border rounded p-2"
    />
    <button @click="submit" class="px-4 py-2 bg-blue-600 text-white rounded">
      Cari
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return { keyword: '' }
  },
  methods: {
    submit() {
      this.$emit('submit', this.keyword)
    }
  }
}
</script>
