<!-- 文件说明：维修员上传维修结果的右侧抽屉，复用在维修工作台和工单列表。 -->
<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { Camera, Close, DocumentChecked } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { updateRepair } from '@/api/repair'
import Upload from '@/views/upload/Upload.vue'

const props = defineProps<{
    modelValue: boolean
    repair?: any | null
}>()

const emit = defineEmits<{
    'update:modelValue': [value: boolean]
    submitted: []
}>()

const submitting = ref(false)
const form = reactive({
    repair_result: '',
    resultImages: [] as string[],
})

const visible = computed({
    get: () => props.modelValue,
    set: (value: boolean) => emit('update:modelValue', value),
})

const repairCode = computed(() => {
    const id = props.repair?.id
    return props.repair?.order_no || props.repair?.code || (id ? `WD${String(id).padStart(12, '0')}` : '未选择工单')
})

const repairRoom = computed(() => {
    const parts = [
        props.repair?.building_name,
        props.repair?.unit_name,
        props.repair?.room_no,
    ].filter(Boolean)

    return parts.length ? parts.join('-') : props.repair?.room || '-'
})

const imageList = computed(() => form.resultImages.map((image) => getFileUrl(image)))

watch(
    () => [visible.value, props.repair?.id],
    () => {
        if (!visible.value) {
            return
        }

        form.repair_result = props.repair?.repair_result || ''
        form.resultImages = [...(props.repair?.result_image_list || [])]
    },
)

const getFileUrl = (url: string) => {
    if (!url) {
        return ''
    }

    return url.startsWith('http') ? url : `http://127.0.0.1:8000${url}`
}

const addResultImage = (url: string) => {
    form.resultImages.push(url)
}

const removeResultImage = (index: number) => {
    form.resultImages.splice(index, 1)
}

const submitResult = async () => {
    if (!props.repair?.id) {
        ElMessage.warning('请先选择需要上传结果的工单')
        return
    }

    if (!form.repair_result.trim()) {
        ElMessage.warning('请填写维修结果说明')
        return
    }

    submitting.value = true

    try {
        await updateRepair(props.repair.id, {
            status: 'finished',
            repair_result: form.repair_result.trim(),
            result_images: form.resultImages.join('|'),
        })

        ElMessage.success('维修结果已提交')
        visible.value = false
        emit('submitted')
    } finally {
        submitting.value = false
    }
}
</script>

<template>
    <el-drawer
        v-model="visible"
        custom-class="repair-result-drawer"
        direction="rtl"
        size="420px"
        :with-header="false"
    >
        <div class="drawer-shell">
            <header class="drawer-header">
                <h2>上传结果</h2>
                <button type="button" aria-label="关闭上传结果" @click="visible = false">
                    <el-icon><Close /></el-icon>
                </button>
            </header>

            <section class="drawer-section">
                <h3>工单信息</h3>
                <div class="repair-summary">
                    <strong>{{ repairCode }}</strong>
                    <span>{{ props.repair?.title || props.repair?.content || '维修工单' }}</span>
                    <p>{{ repairRoom }} ｜ {{ props.repair?.owner_name || props.repair?.owner || '业主' }}</p>
                    <small>预约时间：{{ props.repair?.created_at || props.repair?.time || '-' }}</small>
                </div>
            </section>

            <section class="drawer-step">
                <span class="step-index">1</span>
                <div class="step-content">
                    <h3>拍照上传</h3>
                    <p>请上传现场照片，支持多张图片。</p>
                    <div class="upload-zone">
                        <el-icon><Camera /></el-icon>
                        <Upload
                            upload-type="repair_image"
                            button-text="上传现场照片"
                            @success="addResultImage"
                        />
                        <small>支持 JPG / PNG，单张不超过 10MB</small>
                    </div>
                    <div class="result-images">
                        <div
                            v-for="(image, index) in imageList"
                            :key="image"
                            class="result-image"
                        >
                            <el-image
                                :src="image"
                                :preview-src-list="imageList"
                                fit="cover"
                            />
                            <button type="button" @click="removeResultImage(index)">删除</button>
                        </div>
                        <div
                            v-for="slot in Math.max(0, 4 - imageList.length)"
                            :key="`slot-${slot}`"
                            class="empty-image-slot"
                        >
                            +
                        </div>
                    </div>
                </div>
            </section>

            <section class="drawer-step">
                <span class="step-index">2</span>
                <div class="step-content">
                    <h3>提交结果</h3>
                    <p>请填写维修结果说明。</p>
                    <el-input
                        v-model="form.repair_result"
                        type="textarea"
                        :rows="7"
                        maxlength="500"
                        show-word-limit
                        placeholder="填写维修结果说明"
                    />
                </div>
            </section>
        </div>

        <template #footer>
            <button
                type="button"
                class="submit-result-button"
                :disabled="submitting"
                @click="submitResult"
            >
                <el-icon><DocumentChecked /></el-icon>
                {{ submitting ? '提交中...' : '提交结果' }}
            </button>
        </template>
    </el-drawer>
</template>

<style scoped>
.drawer-shell {
    display: flex;
    flex-direction: column;
    gap: 22px;
    min-height: 100%;
}

.drawer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.drawer-header h2,
.drawer-section h3,
.step-content h3 {
    margin: 0;
    color: var(--text-heading);
    font-size: 18px;
    font-weight: 700;
    line-height: 28px;
}

.drawer-header button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: 0;
    border-radius: 6px;
    color: var(--text-muted);
    background: transparent;
    cursor: pointer;
}

.drawer-header button:hover {
    color: var(--brand-primary);
    background: var(--brand-primary-subtle);
}

.repair-summary {
    display: grid;
    gap: 8px;
    margin-top: 12px;
    padding: 14px 16px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: #fff;
}

.repair-summary strong {
    color: var(--brand-primary);
    font-size: 16px;
    line-height: 24px;
}

.repair-summary span,
.repair-summary p,
.repair-summary small,
.step-content p,
.upload-zone small {
    margin: 0;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 20px;
}

.drawer-step {
    display: grid;
    grid-template-columns: 28px minmax(0, 1fr);
    gap: 14px;
}

.step-index {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    color: #fff;
    background: var(--brand-primary);
    font-size: 14px;
    font-weight: 700;
}

.step-content {
    display: grid;
    gap: 12px;
}

.upload-zone {
    display: grid;
    place-items: center;
    gap: 10px;
    min-height: 150px;
    padding: 18px;
    border: 1px dashed #cbd5e1;
    border-radius: 8px;
    background: var(--brand-primary-subtle);
    text-align: center;
}

.upload-zone > .el-icon {
    color: var(--brand-primary);
    font-size: 40px;
}

.result-images {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
}

.result-image,
.empty-image-slot {
    position: relative;
    display: grid;
    place-items: center;
    aspect-ratio: 1;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background: #fff;
    overflow: hidden;
}

.result-image :deep(.el-image) {
    width: 100%;
    height: 100%;
}

.result-image button {
    position: absolute;
    right: 4px;
    bottom: 4px;
    border: 0;
    border-radius: 4px;
    color: #fff;
    background: rgba(15, 23, 42, 0.66);
    cursor: pointer;
    font-size: 12px;
}

.empty-image-slot {
    color: var(--text-muted);
    font-size: 24px;
}

.submit-result-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    min-height: 46px;
    border: 0;
    border-radius: 6px;
    color: #fff;
    background: linear-gradient(135deg, var(--brand-primary), var(--brand-primary-hover));
    cursor: pointer;
    font-size: 14px;
    font-weight: 700;
    line-height: 20px;
}

.submit-result-button:disabled {
    cursor: not-allowed;
    opacity: 0.72;
}

:global(.repair-result-drawer .el-drawer__body) {
    padding: 24px;
}

:global(.repair-result-drawer .el-drawer__footer) {
    padding: 18px 24px 24px;
    border-top: 1px solid var(--border-soft);
}
</style>
