<template>
  <div v-if="places.length">
    <h2 class="font-semibold mb-2">Hasil Rekomendasi:</h2>
    <ul class="list-disc pl-6">
      <li v-for="p in places" :key="p.Place_Id">
        ⭐ {{ p.Place_Ratings.toFixed(1) }} — {{ p.Place_Name }} ({{ p.City }})
      </li>
    </ul>
  </div>
  <div v-else class="text-gray-500">Tidak ada hasil.</div>
</template>

<script>
export default {
  props: ['places']
}
</script>
