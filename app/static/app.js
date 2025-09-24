// Application state
let currentUser = null;
let authToken = null;

// DOM elements
let authSection, mainSection, userInfo, userName, alertContainer;
let loginTab, registerTab, loginForm, registerForm;
let setPasswordForm, setPasswordSection;
let testPublicBtn,
  testProtectedBtn,
  testUserDataBtn,
  testMixedBtn,
  testWithoutTokenBtn,
  testOutput;
let googleLoginBtn, logoutBtn; // Added these

// Initialization
document.addEventListener("DOMContentLoaded", function () {
  // Assign DOM elements
  authSection = document.getElementById("authSection");
  mainSection = document.getElementById("mainSection");
  userInfo = document.getElementById("userInfo");
  userName = document.getElementById("userName");
  alertContainer = document.getElementById("alertContainer");

  loginTab = document.getElementById("loginTab");
  registerTab = document.getElementById("registerTab");
  loginForm = document.getElementById("loginForm");
  registerForm = document.getElementById("registerForm");

  setPasswordForm = document.getElementById("setPasswordForm");
  setPasswordSection = document.getElementById("setPasswordSection");

  testPublicBtn = document.getElementById("testPublicBtn");
  testProtectedBtn = document.getElementById("testProtectedBtn");
  testUserDataBtn = document.getElementById("testUserDataBtn");
  testMixedBtn = document.getElementById("testMixedBtn");
  testWithoutTokenBtn = document.getElementById("testWithoutTokenBtn");
  testOutput = document.getElementById("testOutput");

  googleLoginBtn = document.getElementById("googleLoginBtn"); // Added
  logoutBtn = document.getElementById("logoutBtn"); // Added

  initializeApp();
  setupEventListeners();
  checkStoredAuth();

  // Ensure loading spinners are hidden on initial load
  if (loginForm) setLoading(loginForm, false);
  if (registerForm) setLoading(registerForm, false);
});

function initializeApp() {
  console.log("Initializing application...");

  // Check for Google callback in URL
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");
  const userId = urlParams.get("user");
  const error = urlParams.get("error");

  if (error) {
    showAlert("Google login error: " + error, "error");
    window.history.replaceState({}, document.title, window.location.pathname);
  } else if (token && userId) {
    handleGoogleCallback(token, userId);
  }
}

function setupEventListeners() {
  // Tabs
  if (loginTab) loginTab.addEventListener("click", () => switchTab("login"));
  if (registerTab)
    registerTab.addEventListener("click", () => switchTab("register"));

  // Forms
  if (loginForm) loginForm.addEventListener("submit", handleLogin);
  if (registerForm) registerForm.addEventListener("submit", handleRegister);
  if (setPasswordForm)
    setPasswordForm.addEventListener("submit", handleSetPassword);

  // Buttons
  // googleLoginBtn and logoutBtn are now assigned globally in DOMContentLoaded
  if (googleLoginBtn)
    googleLoginBtn.addEventListener("click", handleGoogleLogin);
  if (logoutBtn) logoutBtn.addEventListener("click", handleLogout);

  // API tests
  if (testPublicBtn)
    testPublicBtn.addEventListener("click", () =>
      testEndpoint("/api/public", "GET", false)
    );
  if (testProtectedBtn)
    testProtectedBtn.addEventListener("click", () =>
      testEndpoint("/api/protected", "GET", true)
    );
  if (testUserDataBtn)
    testUserDataBtn.addEventListener("click", () =>
      testEndpoint("/api/user-data", "GET", true)
    );
  if (testMixedBtn)
    testMixedBtn.addEventListener("click", () =>
      testEndpoint("/api/mixed", "GET", true)
    );
  if (testWithoutTokenBtn)
    testWithoutTokenBtn.addEventListener("click", () =>
      testEndpoint("/api/protected", "GET", false)
    );
}

function switchTab(tab) {
  if (tab === "login") {
    loginTab.classList.add("border-blue-500", "text-blue-500", "font-semibold");
    loginTab.classList.remove("text-gray-500");
    registerTab.classList.remove(
      "border-blue-500",
      "text-blue-500",
      "font-semibold"
    );
    registerTab.classList.add("text-gray-500");

    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");
  } else {
    registerTab.classList.add(
      "border-blue-500",
      "text-blue-500",
      "font-semibold"
    );
    registerTab.classList.remove("text-gray-500");
    loginTab.classList.remove(
      "border-blue-500",
      "text-blue-500",
      "font-semibold"
    );
    loginTab.classList.add("text-gray-500");

    registerForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
  }
}

function showAlert(message, type = "info") {
  const alertTypes = {
    success: "bg-green-100 border-green-400 text-green-700",
    error: "bg-red-100 border-red-400 text-red-700",
    warning: "bg-yellow-100 border-yellow-400 text-yellow-700",
    info: "bg-blue-100 border-blue-400 text-blue-700",
  };

  const icons = {
    success: "fas fa-check-circle",
    error: "fas fa-exclamation-circle",
    warning: "fas fa-exclamation-triangle",
    info: "fas fa-info-circle",
  };

  const alert = document.createElement("div");
  alert.className = `alert border px-4 py-3 rounded mb-4 ${alertTypes[type]}`;
  alert.innerHTML = `
        <div class="flex items-center">
            <i class="${icons[type]} mr-2"></i>
            <span>${message}</span>
            <button class="ml-auto" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

  alertContainer.appendChild(alert);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (alert.parentElement) {
      alert.remove();
    }
  }, 5000);
}

function setLoading(form, loading) {
  const button = form.querySelector('button[type="submit"]');
  if (!button) return;

  const btnText = button.querySelector(".btn-text");
  const loadingSpinner = button.querySelector(".loading");

  if (loading) {
    button.disabled = true;
    if (btnText) btnText.style.display = "none";
    if (loadingSpinner) loadingSpinner.style.display = "inline-block";
  } else {
    button.disabled = false;
    if (btnText) btnText.style.display = "inline"; // span is inline by default
    if (loadingSpinner) loadingSpinner.style.display = "none";
  }
}

async function handleLogin(e) {
  e.preventDefault();
  setLoading(loginForm, true);

  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  try {
    const response = await fetch("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (data.success) {
      showAlert(data.message, "success");
      setAuthData(data.data.user, data.data.token);
      showMainSection();
    } else {
      showAlert(data.message, "error");
    }
  } catch (error) {
    showAlert("Connection error: " + error.message, "error");
  } finally {
    setLoading(loginForm, false);
  }
}

async function handleRegister(e) {
  e.preventDefault();
  setLoading(registerForm, true);

  const name = document.getElementById("registerName").value;
  const email = document.getElementById("registerEmail").value;
  const password = document.getElementById("registerPassword").value;

  try {
    const response = await fetch("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });

    const data = await response.json();

    if (data.success) {
      showAlert(data.message, "success");
      setAuthData(data.data.user, data.data.token);
      showMainSection();
    } else {
      showAlert(data.message, "error");
    }
  } catch (error) {
    showAlert("Connection error: " + error.message, "error");
  } finally {
    setLoading(registerForm, false);
  }
}

async function handleSetPassword(e) {
  e.preventDefault();

  const password = document.getElementById("newPassword").value;

  if (password.length < 6) {
    showAlert("Password must be at least 6 characters long", "error");
    return;
  }

  try {
    const response = await fetch("/auth/set-password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({ password }),
    });

    const data = await response.json();

    if (data.success) {
      showAlert(data.message, "success");
      currentUser.has_password = true;
      updateUserProfile();
      setPasswordSection.classList.add("hidden");
    } else {
      showAlert(data.message, "error");
    }
  } catch (error) {
    showAlert("Connection error: " + error.message, "error");
  }
}

function handleGoogleLogin() {
  // Check for Google callback parameters in URL
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get("token");
  const userId = urlParams.get("user");
  const error = urlParams.get("error");

  if (error) {
    showAlert("Google login error: " + error, "error");
    // Clear URL
    window.history.replaceState({}, document.title, window.location.pathname);
    return;
  }

  if (token && userId) {
    // Process Google callback
    handleGoogleCallback(token, userId);
    return;
  }

  // Redirect to Google OAuth
  window.location.href = "/auth/google/login";
}

async function handleGoogleCallback(token, userId) {
  try {
    // Validate received token
    const response = await fetch("/auth/validate-token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    });

    const data = await response.json();

    if (data.success) {
      setAuthData(data.data.user, token);
      showMainSection();
      showAlert("Google login successful!", "success");
    } else {
      showAlert("Token validation error: " + data.message, "error");
    }
  } catch (error) {
    showAlert("Error processing Google callback: " + error.message, "error");
  } finally {
    // Clear URL
    window.history.replaceState({}, document.title, window.location.pathname);
  }
}

function handleLogout() {
  localStorage.removeItem("authToken");
  localStorage.removeItem("currentUser");
  currentUser = null;
  authToken = null;

  showAuthSection();
  showAlert("Logout successful", "success");
}

function setAuthData(user, token) {
  currentUser = user;
  authToken = token;

  // Save to localStorage
  localStorage.setItem("authToken", token);
  localStorage.setItem("currentUser", JSON.stringify(user));
}

function checkStoredAuth() {
  const storedToken = localStorage.getItem("authToken");
  const storedUser = localStorage.getItem("currentUser");

  if (storedToken && storedUser) {
    authToken = storedToken;
    currentUser = JSON.parse(storedUser);

    // Validate token
    validateToken(storedToken);
  }
}

async function validateToken(token) {
  try {
    const response = await fetch("/auth/validate-token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    });

    const data = await response.json();

    if (data.success) {
      showMainSection();
    } else {
      // Invalid token, clear data
      handleLogout();
    }
  } catch (error) {
    console.error("Error validating token:", error);
    handleLogout();
  }
}

function showAuthSection() {
  if (authSection) authSection.classList.remove("hidden");
  if (mainSection) mainSection.classList.add("hidden");
  if (userInfo) userInfo.classList.add("hidden");
}

function showMainSection() {
  if (authSection) authSection.classList.add("hidden");
  if (mainSection) mainSection.classList.remove("hidden");
  if (userInfo) userInfo.classList.remove("hidden");

  updateUserInfo();
  updateUserProfile();
}

function updateUserInfo() {
  if (currentUser && userName) {
    userName.textContent = currentUser.name || currentUser.email;
  }
}

function updateUserProfile() {
  const userProfile = document.getElementById("userProfile");

  if (currentUser && userProfile) {
    userProfile.innerHTML = `
            <div class="flex items-center space-x-3 p-3 bg-gray-50 rounded-md">
                <i class="fas fa-user-circle text-2xl text-gray-600"></i>
                <div>
                    <p class="font-semibold">${currentUser.name || "User"}</p>
                    <p class="text-sm text-gray-600">${currentUser.email}</p>
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4 mt-4">
                <div class="text-center p-3 bg-blue-50 rounded-md">
                    <i class="fas fa-key text-blue-600 mb-2"></i>
                    <p class="text-sm font-semibold">Password</p>
                    <p class="text-xs ${
                      currentUser.has_password
                        ? "text-green-600"
                        : "text-red-600"
                    }">
                        ${currentUser.has_password ? "Set" : "Not set"}
                    </p>
                </div>
                <div class="text-center p-3 bg-green-50 rounded-md">
                    <i class="fab fa-google text-green-600 mb-2"></i>
                    <p class="text-sm font-semibold">Google</p>
                    <p class="text-xs ${
                      currentUser.uid ? "text-green-600" : "text-gray-600"
                    }">
                        ${currentUser.uid ? "Connected" : "Not connected"}
                    </p>
                </div>
            </div>
        `;

    // Show set password section if needed
    if (currentUser.uid && !currentUser.has_password && setPasswordSection) {
      setPasswordSection.classList.remove("hidden");
    } else if (setPasswordSection) {
      setPasswordSection.classList.add("hidden");
    }
  }
}

async function testEndpoint(endpoint, method = "GET", useToken = false) {
  const timestamp = new Date().toLocaleTimeString();

  addTestOutput(
    `[${timestamp}] Testing ${method} ${endpoint}${
      useToken ? " (with token)" : " (without token)"
    }...`
  );

  try {
    const headers = {
      "Content-Type": "application/json",
    };

    if (useToken && authToken) {
      headers["Authorization"] = `Bearer ${authToken}`;
    }

    const response = await fetch(endpoint, {
      method,
      headers,
    });

    const data = await response.json();

    const statusColor = response.ok ? "text-green-400" : "text-red-400";
    addTestOutput(
      `<span class="${statusColor}">Status: ${response.status} ${response.statusText}</span>`
    );
    addTestOutput(`Response: ${JSON.stringify(data, null, 2)}`);
  } catch (error) {
    addTestOutput(`<span class="text-red-400">Error: ${error.message}</span>`);
  }

  addTestOutput("---");
}

function addTestOutput(message) {
  if (!testOutput) return;

  // Clear initial message if exists
  if (testOutput.textContent.includes("Click the buttons")) {
    testOutput.innerHTML = "";
  }

  const line = document.createElement("div");
  line.innerHTML = message;
  testOutput.appendChild(line);

  // Scroll to bottom
  testOutput.scrollTop = testOutput.scrollHeight;
}
