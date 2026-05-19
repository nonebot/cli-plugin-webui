import { defineStore } from "pinia";
import { ref } from "vue";

interface DataTypeFields {
  [key: string]: (number | string)[];
}

type DataState<T extends DataTypeFields> = {
  [key: string]: T;
};

export const useChartStore = defineStore("chartStore", () => {
  const chartDataMaxLength = ref(100);

  const initArr = (defaultData: any = 0) =>
    Array.from({ length: chartDataMaxLength.value }, () => defaultData);

  const limitArrayLength = (arr: any[], maxLength: number) => {
    while (arr.length > maxLength) {
      arr.shift();
    }
  };

  const dataRefs = ref<Partial<DataState<DataTypeFields>>>({});

  const dataCreators: { [key: string]: () => DataTypeFields } = {};

  const updateData = <T extends keyof DataTypeFields>(
    dataType: T,
    field: T,
    v: DataTypeFields[T][number],
    maxLength: number = chartDataMaxLength.value,
  ) => {
    const data = dataRefs.value[dataType];
    if (!data) return;

    data[field].push(v);
    limitArrayLength(data[field], maxLength);
    dataRefs.value[dataType] = { ...data };
  };

  const addDataType = <T extends DataTypeFields>(dataType: string, fields: T) => {
    const createDefault = () => {
      const defaultFields: { [key in keyof T]: T[key] } = {} as any;
      for (const key in fields) {
        defaultFields[key] = initArr(fields[key][0]) as T[Extract<keyof T, string>];
      }
      return defaultFields;
    };
    if (dataRefs.value[dataType]) return;
    dataRefs.value[dataType] = createDefault();
    dataCreators[dataType] = createDefault;
  };

  const resetData = (dataType: string) => {
    const data = dataCreators[dataType]?.();
    dataRefs.value[dataType] = data;
  };

  return {
    chartDataMaxLength,
    dataRefs,
    updateData,
    addDataType,
    resetData,
  };
});
