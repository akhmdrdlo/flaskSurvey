let questions = [];

fetch("../static/questions.json")
  .then(response => response.json())
  .then(data => {
    questions = data;
    
  })
  .catch(error => console.error("Gagal mengambil pertanyaan:", error));

let currentPage = 0;
const perPage = 10;
let answers = {};
let selectedRole = "";

let groupedBySection = [];

function mulaiSurvey() {
  if (questions.length === 0) {
    alert("Pertanyaan belum siap dimuat.");
    return;
  }

  const nama = document.getElementById("nama").value;
  selectedRole = document.getElementById("role").value;
  const provinsiSelect = document.getElementById("select-provinsi");
  const kabupatenSelect = document.getElementById("select-kabupaten");
  const kelas = document.querySelector('input[name="kelas"]:checked')?.value;

  if (!nama || !selectedRole || !provinsiSelect.value || !kabupatenSelect.value || (selectedRole !== "guru" && !kelas)) {
    const toast = document.createElement("div");
    toast.className = "toast fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-lg opacity-0 transition-opacity duration-300";
    toast.innerText = "Harap isi identitas lengkap terlebih dahulu (Nama, Role, Provinsi, Kabupaten, dan Kelas jika bukan guru).";
    document.body.appendChild(toast);

    // Trigger fade-in animation
    setTimeout(() => {
      toast.classList.add("opacity-100");
    }, 10);

    // Remove toast after 3 seconds
    setTimeout(() => {
      toast.classList.remove("opacity-100");
      setTimeout(() => {
        toast.remove();
      }, 300); // Wait for fade-out animation to complete
    }, 3000);

    return;
  }

  provinsiSelect.addEventListener('change', function() {
    const selectedText = this.options[this.selectedIndex].text;
    answers.provinsi = selectedText;
  });

  kabupatenSelect.addEventListener('change', function() {
    const selectedText = this.options[this.selectedIndex].text;
    answers.kabupaten = selectedText;
  });

  answers["nama"] = nama;
  answers["role"] = selectedRole;
  answers["provinsi"] = provinsiSelect.options[provinsiSelect.selectedIndex].text;
  answers["kabupaten"] = kabupatenSelect.options[kabupatenSelect.selectedIndex].text;

  if (selectedRole !== "guru") {
    answers["kelas"] = kelas;
  }

  localStorage.setItem("surveyAnswers", JSON.stringify(answers));
  document.getElementById("form-identitas").classList.add("hidden");
  document.getElementById("form-survey").classList.remove("hidden");
  renderQuestions();
}

  
  function renderQuestions() {
    const container = document.getElementById("surveyForm");
    container.innerHTML = "";
  
    const visibleQuestions = questions.filter(q => {
      if (q.role === "all") return true;
      if (q.role === "MTs_MA" && ["MTs", "MA"].includes(selectedRole)) return true;
      if (q.role === "guru" && selectedRole === "guru") return true;
      if (q.role === selectedRole) return true;
      return false;
    });
  
    groupedBySection = [];
    let lastSection = null;
    visibleQuestions.forEach(q => {
      if (q.section !== lastSection) {
        groupedBySection.push([]);
        lastSection = q.section;
      }
      groupedBySection[groupedBySection.length - 1].push(q);
    });
  
    const section = groupedBySection[currentPage];
    if (!section) return;
  
    const sectionTitle = document.createElement("div");
    sectionTitle.className = "text-xl font-semibold text-blue-700 border-b mb-4 pb-2 text-center";
    sectionTitle.innerText = section[0].section;
    container.appendChild(sectionTitle);

  section.forEach(q => {
    const wrapper = document.createElement("div");
    wrapper.className = "mb-8";
    wrapper.innerHTML = `<p class='text-md font-medium text-gray-800'>${q.pertanyaan}</p>`;

    if (q.tipe === "text") {
      wrapper.innerHTML += `<input type='text' name='q${q.id}' class='w-full p-2 border rounded-md' value='${answers[`q${q.id}`] || ""}'>`;
    } else if (q.tipe === "radio") {
      const radioContainer = document.createElement("div");
      radioContainer.className = "flex flex-wrap gap-4";

      q.opsi.forEach(opt => {
      const checked = answers[`q${q.id}`] === opt ? "checked" : "";
      const radioWrapper = document.createElement("label");
      radioWrapper.className = "flex items-center gap-2";
      radioWrapper.innerHTML = `<input type='radio' name='q${q.id}' value='${opt}' ${checked} class='mr-2'>${opt}`;
      radioContainer.appendChild(radioWrapper);
      });

      wrapper.appendChild(radioContainer);
    } else if (q.tipe === "checkbox") {
      q.opsi.forEach(opt => {
      const isChecked = (answers[`q${q.id}`] || []).includes(opt);
      wrapper.innerHTML += `<label class='block'><input type='checkbox' name='q${q.id}' value='${opt}' ${isChecked ? "checked" : ""} class='mr-2'>${opt}</label>`;
      if (opt === "Lainnya") {
        wrapper.innerHTML += `<input type='text' name='q${q.id}_lainnya' value='${answers[`q${q.id}_lainnya`] || ""}' class='w-full p-2 mt-2 border rounded-md' placeholder='Tulis lainnya jika ada'>`;
      }
      });
    }
    else if (q.tipe === "textarea") {
      wrapper.innerHTML += `<textarea name='q${q.id}' class='w-full p-2 border rounded-md' rows='4'>${answers[`q${q.id}`] || ""}</textarea>`;
    }
  
    const separator = document.createElement("hr");
    separator.className = "my-6 border-gray-300";

    container.appendChild(wrapper);
    container.appendChild(separator);

  });

  const nextBtn = document.getElementById("next-btn");
  const prevBtn = document.getElementById("prev-btn");
  const lastPage = groupedBySection.length - 1;

  nextBtn.textContent = currentPage === lastPage ? "Kirim Survey" : "Selanjutnya";
  nextBtn.classList.toggle("bg-blue-700", currentPage === lastPage);
  nextBtn.classList.toggle("bg-blue-500", currentPage !== lastPage);
  prevBtn.disabled = currentPage === 0;

  document.getElementById("progress-indicator").textContent = `Halaman ${currentPage + 1} dari ${groupedBySection.length}`;
  document.getElementById("progress-bar").style.width = `${((currentPage + 1) / groupedBySection.length) * 100}%`;
  }
  function validateCurrentPage() {
  const section = groupedBySection[currentPage];
  if (!section) return false;

  for (const q of section) {
    const name = `q${q.id}`;
    if (q.tipe === "radio") {
      const checked = document.querySelector(`input[name="${name}"]:checked`);
      if (!checked) return false;
    }
    else if (q.tipe === "text" || q.tipe === "textarea") {
      const input = document.querySelector(`input[name="${name}"], textarea[name="${name}"]`);
      if (!input || input.value.trim() === "") return false;
    }
    else if (q.tipe === "checkbox") {
      const checked = document.querySelectorAll(`input[name="${name}"]:checked`);
      if (checked.length === 0) return false;
    }
  }

  return true;
}


  function saveAnswers() {
    const inputs = document.querySelectorAll("#surveyForm input:checked, #surveyForm select, #surveyForm input[type='text'], #surveyForm textarea");
    inputs.forEach(input => {
      const name = input.name;
      const value = input.value;
      if (answers[name]) {
        if (Array.isArray(answers[name])) {
          if (!answers[name].includes(value)) {
            answers[name].push(value);
          }
        } else if (answers[name] !== value) {
          answers[name] = [answers[name], value];
        }
      } else {
        answers[name] = value;
      }
    });
    localStorage.setItem("surveyAnswers", JSON.stringify(answers));
  }
  
  function submitSurvey() {
    saveAnswers();
    console.log("Data dikirim:", answers);
  
    fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(answers)
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        document.getElementById('loadingSpinner').classList.remove('hidden');
        setTimeout(() => {
          localStorage.removeItem("surveyAnswers");
          window.location.href = data.redirect;
        }, 2000);
      } else {
        alert("Gagal mengirim survey. Silakan coba lagi.");
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert("Terjadi kesalahan saat mengirim data.");
    });
  }
  
  
  

