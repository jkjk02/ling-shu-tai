<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, shallowRef, watch } from 'vue';
import * as monaco from 'monaco-editor/esm/vs/editor/editor.api';
import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';

import 'monaco-editor/esm/vs/basic-languages/markdown/markdown.contribution';
import 'monaco-editor/esm/vs/basic-languages/python/python.contribution';
import 'monaco-editor/esm/vs/basic-languages/shell/shell.contribution';
import 'monaco-editor/min/vs/editor/editor.main.css';
import 'monaco-editor/esm/vs/language/json/monaco.contribution';

const props = withDefaults(
  defineProps<{
    modelValue: string;
    language?: string;
    height?: number | string;
    readonly?: boolean;
    minimap?: boolean;
  }>(),
  {
    language: 'plaintext',
    height: 320,
    readonly: false,
    minimap: false,
  },
);

const emit = defineEmits<{
  'update:modelValue': [value: string];
  blur: [];
  change: [value: string];
}>();

const containerRef = ref<HTMLDivElement>();
const editorRef = shallowRef<monaco.editor.IStandaloneCodeEditor>();
const isApplyingExternalValue = ref(false);

const heightStyle = computed(() => (typeof props.height === 'number' ? `${props.height}px` : props.height));

const globalScope = globalThis as typeof globalThis & {
  MonacoEnvironment?: {
    getWorker: (_workerId: string, label: string) => Worker;
  };
};

if (!globalScope.MonacoEnvironment) {
  globalScope.MonacoEnvironment = {
    getWorker(_workerId: string, label: string) {
      if (label === 'json') {
        return new jsonWorker();
      }
      return new editorWorker();
    },
  };
}

function createEditor() {
  if (!containerRef.value) {
    return;
  }

  const editor = monaco.editor.create(containerRef.value, {
    value: props.modelValue,
    language: props.language,
    theme: 'vs',
    readOnly: props.readonly,
    automaticLayout: true,
    minimap: {
      enabled: props.minimap,
    },
    fontSize: 13,
    lineHeight: 20,
    lineNumbersMinChars: 3,
    scrollBeyondLastLine: false,
    roundedSelection: true,
    wordWrap: 'on',
    tabSize: 2,
    insertSpaces: true,
    padding: {
      top: 14,
      bottom: 14,
    },
  });

  editor.onDidChangeModelContent(() => {
    if (isApplyingExternalValue.value) {
      return;
    }
    const value = editor.getValue();
    emit('update:modelValue', value);
    emit('change', value);
  });

  editor.onDidBlurEditorText(() => {
    emit('blur');
  });

  editorRef.value = editor;
}

function disposeEditor() {
  editorRef.value?.dispose();
  editorRef.value = undefined;
}

onMounted(async () => {
  await nextTick();
  createEditor();
});

onBeforeUnmount(() => {
  disposeEditor();
});

watch(
  () => props.modelValue,
  (value) => {
    const editor = editorRef.value;
    if (!editor || editor.getValue() === value) {
      return;
    }
    isApplyingExternalValue.value = true;
    editor.setValue(value);
    isApplyingExternalValue.value = false;
  },
);

watch(
  () => props.language,
  (language) => {
    const model = editorRef.value?.getModel();
    if (!model) {
      return;
    }
    monaco.editor.setModelLanguage(model, language);
  },
);

watch(
  () => props.readonly,
  (readonly) => {
    editorRef.value?.updateOptions({ readOnly: readonly });
  },
);

watch(
  () => props.minimap,
  (minimap) => {
    editorRef.value?.updateOptions({ minimap: { enabled: minimap } });
  },
);
</script>

<template>
  <div class="monaco-code-editor" :style="{ height: heightStyle }">
    <div ref="containerRef" class="monaco-code-editor__surface" />
  </div>
</template>

<style scoped>
.monaco-code-editor {
  width: 100%;
  min-height: 180px;
  overflow: hidden;
  border: 1px solid var(--el-border-color);
  border-radius: 14px;
  background: #ffffff;
}

.monaco-code-editor__surface {
  width: 100%;
  height: 100%;
}
</style>
