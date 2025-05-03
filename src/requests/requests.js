export const sendRequest = async ({ operation, imageFile, secondImageFile, params }) => {
  const formData = new FormData();
  formData.append("file", imageFile);

  // Aritmetik işlemler için ikinci görsel
  if (operation === "arithmetic" && secondImageFile) {
    formData.append("file2", secondImageFile);
  }

  // Parametreleri özel durumlara göre ekle
  if (params && typeof params === "object") {
    if (operation === "noise") {
      // Gürültü işlemi için özel parametre adları
      formData.append("salt_amount", params.salt_amount || 0.05);
      formData.append("pepper_amount", params.pepper_amount || 0.05);
    } else {
      for (const key in params) {
        if (params[key] !== undefined && params[key] !== null) {
          formData.append(key, params[key]);
        }
      }
    }
  }

  try {
    const response = await fetch(`http://127.0.0.1:8001/process/${operation}`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Sunucu hatası");
    }

    const blob = await response.blob();
    return { url: URL.createObjectURL(blob) };
  } catch (error) {
    console.error("İstek başarısız:", error);
    return null;
  }
};
