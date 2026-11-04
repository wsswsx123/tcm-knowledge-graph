<template>
  <div class="medical-disclaimer">
    <span class="icon">⚕</span>
    本内容基于体质测评与知识图谱自动生成，仅供日常养生参考，不构成医疗建议；
    如有身体不适或疾病，请及时就医并遵医嘱。
  </div>
</template>

<script setup>
</script>

<style scoped>
.medical-disclaimer {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 12px 0;
  padding: 8px 12px;
  border-radius: 8px;
  background: #fff7ed;
  border: 1px solid #fed7aa;
  color: #9a3412;
  font-size: 12px;
  line-height: 1.5;
}
.icon { flex-shrink: 0; }
</style>
