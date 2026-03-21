<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  status: 'ready' | 'warning' | 'missing';
}>();

const label = computed(() => {
  if (props.status === 'ready') return '正常';
  if (props.status === 'warning') return '待检查';
  return '未发现';
});
</script>

<template>
  <span class="status-pill" :data-status="status">{{ label }}</span>
</template>
