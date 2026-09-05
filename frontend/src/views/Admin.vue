<template>
  <div class="bg-white rounded-sm shadow-lg p-8 border border-border relative">
    <!-- 删除节点确认对话框 -->
    <div v-if="nodeToDelete" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-sm shadow-xl max-w-sm w-full border border-border">
        <h3 class="text-xl font-serif font-bold text-secondary mb-4">确认删除</h3>
        <p class="text-[#6b5c51] mb-8 font-serif">确定要删除该节点吗？此操作不可恢复。</p>
        <div class="flex justify-end space-x-4">
          <button @click="nodeToDelete = null" class="px-4 py-2 text-[#6b5c51] hover:bg-paper rounded-sm font-serif">取消</button>
          <button @click="confirmDeleteNode" class="px-4 py-2 bg-red-700 text-white rounded-sm hover:bg-red-800 font-serif">确定删除</button>
        </div>
      </div>
    </div>

    <!-- 添加/编辑节点模态框 -->
    <div v-if="showNodeModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-sm shadow-xl max-w-md w-full border border-border">
        <h3 class="text-xl font-serif font-bold text-secondary mb-4">{{ isEditMode ? '编辑节点' : '添加节点' }}</h3>
        <form @submit.prevent="submitNode">
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">节点ID</label>
            <input v-model="newNode.id" type="text" required :disabled="isEditMode" class="w-full p-2 border border-border rounded-sm" :class="{ 'bg-gray-100': isEditMode }">
            <p v-if="isEditMode" class="text-xs text-gray-500 mt-1">ID不可修改</p>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">标签</label>
            <select v-model="newNode.label" required :disabled="isEditMode" class="w-full p-2 border border-border rounded-sm" :class="{ 'bg-gray-100': isEditMode }">
              <option value="Constitution">体质 (Constitution)</option>
              <option value="Acupoint">穴位 (Acupoint)</option>
              <option value="Food">食材 (Food)</option>
              <option value="Exercise">运动 (Exercise)</option>
            </select>
            <p v-if="isEditMode" class="text-xs text-gray-500 mt-1">标签不可修改</p>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">名称</label>
            <input v-model="newNode.name" type="text" required class="w-full p-2 border border-border rounded-sm">
          </div>
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">属性 (JSON格式)</label>
            <textarea v-model="newNode.properties" rows="4" class="w-full p-2 border border-border rounded-sm font-mono text-sm" placeholder='{"description": "..."}'></textarea>
          </div>
          <div class="flex justify-end space-x-4">
            <button type="button" @click="showNodeModal = false" class="px-4 py-2 text-[#6b5c51] hover:bg-paper rounded-sm font-serif">取消</button>
            <button type="submit" class="px-4 py-2 bg-primary text-white rounded-sm hover:bg-secondary font-serif">{{ isEditMode ? '保存修改' : '确定添加' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 添加关系模态框 -->
    <div v-if="showEdgeModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white p-8 rounded-sm shadow-xl max-w-md w-full border border-border">
        <h3 class="text-xl font-serif font-bold text-secondary mb-4">添加关系</h3>
        <form @submit.prevent="submitEdge">
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">源节点ID</label>
            <input v-model="newEdge.source" type="text" required class="w-full p-2 border border-border rounded-sm">
          </div>
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">目标节点ID</label>
            <input v-model="newEdge.target" type="text" required class="w-full p-2 border border-border rounded-sm">
          </div>
          <div class="mb-4">
            <label class="block text-sm font-serif text-secondary mb-1">关系类型</label>
            <select v-model="newEdge.type" required class="w-full p-2 border border-border rounded-sm">
              <option value="RECOMMEND_ACUPOINT">RECOMMEND_ACUPOINT</option>
              <option value="RECOMMEND_FOOD">RECOMMEND_FOOD</option>
              <option value="RECOMMEND_EXERCISE">RECOMMEND_EXERCISE</option>
            </select>
          </div>
          <div class="flex justify-end space-x-4">
            <button type="button" @click="showEdgeModal = false" class="px-4 py-2 text-[#6b5c51] hover:bg-paper rounded-sm font-serif">取消</button>
            <button type="submit" class="px-4 py-2 bg-primary text-white rounded-sm hover:bg-secondary font-serif">确定添加</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 主标题 -->
    <h2 class="text-3xl font-serif font-bold text-secondary mb-8 border-b-2 border-border pb-4 tracking-widest">
      <span class="text-primary mr-2">❖</span>图谱管理后台
    </h2>

    <!-- 节点管理 -->
    <div class="mb-12">
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-serif font-bold text-primary">节点管理</h3>
        <button @click="openAddNode" class="bg-primary text-white px-5 py-2 rounded-sm flex items-center hover:bg-secondary font-serif">
          <Plus class="w-4 h-4 mr-1" /> 添加节点
        </button>
      </div>
      <div class="overflow-x-auto border border-border rounded-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-paper text-secondary border-b border-border font-serif">
            <tr>
              <th class="p-4 font-bold">ID</th>
              <th class="p-4 font-bold">名称</th>
              <th class="p-4 font-bold">类别</th>
              <th class="p-4 font-bold">属性</th>
              <th class="p-4 font-bold">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="n in nodes" :key="n.id" class="border-b border-[#f5f0e6] hover:bg-paper">
              <td class="p-4 text-sm text-primary font-mono">{{ n.id }}</td>
              <td class="p-4 font-bold text-ink font-serif">{{ n.name || '未命名' }}</td>
              <td class="p-4 text-sm">
                <span :class="[
                  'px-3 py-1 rounded-sm text-xs font-serif border',
                  n.label === 'Constitution' ? 'bg-[#8b3a3a]/10 text-[#8b3a3a] border-[#8b3a3a]/20' :
                  n.label === 'Acupoint' ? 'bg-[#b8860b]/10 text-[#b8860b] border-[#b8860b]/20' :
                  n.label === 'Food' ? 'bg-[#556b2f]/10 text-[#556b2f] border-[#556b2f]/20' :
                  n.label === 'Exercise' ? 'bg-[#4682b4]/10 text-[#4682b4] border-[#4682b4]/20' :
                  'bg-[#c0b298]/10 text-[#c0b298] border-[#c0b298]/20'
                ]">{{ n.label }}</span>
              </td>
              <td class="p-4 text-sm text-[#6b5c51] max-w-xs truncate">{{ n.properties }}</td>
              <td class="p-4">
                <div class="flex space-x-3">
                  <!-- 编辑按钮绑定点击事件 -->
                  <button @click="openEditNode(n)" class="text-primary hover:text-secondary"><Edit class="w-5 h-5" /></button>
                  <button @click="handleDeleteNode(n.id)" class="text-red-700 hover:text-red-900"><Trash2 class="w-5 h-5" /></button>
                </div>
              </td>
            </tr>
            <tr v-if="!nodes.length">
              <td colspan="5" class="p-4 text-center text-[#c0b298] font-serif">暂无节点数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 关系管理 -->
    <div>
      <div class="flex justify-between items-center mb-6">
        <h3 class="text-xl font-serif font-bold text-primary">关系管理</h3>
        <button @click="openAddEdge" class="bg-primary text-white px-5 py-2 rounded-sm flex items-center hover:bg-secondary font-serif">
          <Plus class="w-4 h-4 mr-1" /> 添加关系
        </button>
      </div>
      <div class="overflow-x-auto border border-border rounded-sm">
        <table class="w-full text-left border-collapse">
          <thead class="bg-paper text-secondary border-b border-border font-serif">
            <tr>
              <th class="p-4 font-bold">ID</th>
              <th class="p-4 font-bold">源节点</th>
              <th class="p-4 font-bold">关系类型</th>
              <th class="p-4 font-bold">目标节点</th>
              <th class="p-4 font-bold">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in edges" :key="e.id" class="border-b border-[#f5f0e6] hover:bg-paper">
              <td class="p-4 text-sm text-primary font-mono">{{ e.id }}</td>
              <td class="p-4 font-bold text-ink font-serif">{{ e.source }}</td>
              <td class="p-4 text-sm text-[#6b5c51] font-serif"><span class="bg-paper px-2 py-1 rounded-sm border border-border">{{ e.type }}</span></td>
              <td class="p-4 font-bold text-ink font-serif">{{ e.target }}</td>
              <td class="p-4">
                <button class="text-red-700 hover:text-red-900"><Trash2 class="w-5 h-5" /></button>
              </td>
            </tr>
            <tr v-if="!edges.length">
              <td colspan="5" class="p-4 text-center text-[#c0b298] font-serif">暂无关系数据</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Trash2, Edit } from 'lucide-vue-next'
import axios from 'axios'

// 数据
const nodes = ref([])
const edges = ref([])
const loading = ref(true)
const nodeToDelete = ref(null)

// 控制模态框显示
const showNodeModal = ref(false)
const showEdgeModal = ref(false)
const isEditMode = ref(false) // 是否是编辑模式

// 新节点数据（添加或编辑时使用）
const newNode = ref({
  id: '',
  label: 'Constitution',
  name: '',
  properties: '{}'
})

// 新关系数据
const newEdge = ref({
  source: '',
  target: '',
  type: 'RECOMMEND_ACUPOINT'
})

// 获取数据
const fetchData = async () => {
  try {
    const res = await axios.get('/api/admin/graph')
    nodes.value = res.data.nodes || []
    edges.value = res.data.edges || []
  } catch (error) {
    console.error('获取图谱数据失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

// 打开添加节点模态框
const openAddNode = () => {
  isEditMode.value = false
  newNode.value = { id: '', label: 'Constitution', name: '', properties: '{}' }
  showNodeModal.value = true
}

// 打开编辑节点模态框
const openEditNode = (node) => {
  isEditMode.value = true
  // 复制节点数据到表单，属性字符串化
  newNode.value = {
    id: node.id,
    label: node.label,
    name: node.name || '',
    properties: JSON.stringify(node.properties || {}, null, 2)
  }
  showNodeModal.value = true
}

// 打开添加关系模态框
const openAddEdge = () => {
  newEdge.value = { source: '', target: '', type: 'RECOMMEND_ACUPOINT' }
  showEdgeModal.value = true
}

// 提交节点（新增或编辑）
const submitNode = async () => {
  try {
    let props = {}
    try {
      props = JSON.parse(newNode.value.properties)
    } catch (e) {
      alert('属性不是合法的 JSON 格式')
      return
    }

    if (isEditMode.value) {
      // 编辑节点：调用 PUT 接口
      await axios.put(`/api/admin/node/${newNode.value.id}`, {
        name: newNode.value.name,
        properties: props
      })
    } else {
      // 新增节点：调用 POST 接口
      await axios.post('/api/admin/node', {
        id: newNode.value.id,
        label: newNode.value.label,
        name: newNode.value.name,
        properties: props
      })
    }

    fetchData()
    showNodeModal.value = false
  } catch (error) {
    console.error('保存节点失败:', error)
    alert('保存节点失败: ' + (error.response?.data?.error || error.message))
  }
}

// 提交新关系
const submitEdge = async () => {
  try {
    await axios.post('/api/admin/edge', {
      source: newEdge.value.source,
      target: newEdge.value.target,
      type: newEdge.value.type
    })
    fetchData()
    showEdgeModal.value = false
  } catch (error) {
    console.error('添加关系失败:', error)
    alert('添加关系失败: ' + (error.response?.data?.error || error.message))
  }
}

// 处理删除节点
const handleDeleteNode = (id) => {
  nodeToDelete.value = id
}

const confirmDeleteNode = async () => {
  try {
    await axios.delete(`/api/admin/node/${nodeToDelete.value}`)
    nodes.value = nodes.value.filter(n => n.id !== nodeToDelete.value)
    edges.value = edges.value.filter(e => e.source !== nodeToDelete.value && e.target !== nodeToDelete.value)
  } catch (error) {
    console.error('删除节点失败:', error)
  } finally {
    nodeToDelete.value = null
  }
}
</script>