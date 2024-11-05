<script setup lang="ts">
import { editor as monacoEditor } from "monaco-editor/esm/vs/editor/editor.api.js";
import { onMounted, ref, watch } from "vue";

const props = defineProps<{
  modelValue: string;
  editorOptional: Partial<monacoEditor.IStandaloneEditorConstructionOptions>;
}>();

const emit = defineEmits<{
  editor: [value: monacoEditor.IStandaloneCodeEditor];
  updateValue: [value: string];
}>();

const editorContainer = ref<HTMLDivElement>();
let editor: monacoEditor.IStandaloneCodeEditor;

onMounted(() => {
  editor = monacoEditor.create(editorContainer.value!, {
    value: props.modelValue,
    ...props.editorOptional,
  });
  emit("editor", editor);
  editor.onDidChangeModelContent(() => {
    emit("updateValue", editor.getValue());
  });
});

watch(
  () => props.modelValue,
  (value) => editor.setValue(value),
);
</script>

<template>
  <div ref="editorContainer"></div>
</template>
