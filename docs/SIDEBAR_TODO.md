# 📋 Sidebar Implementation TODO

**Goal:** Add a premium slide‑out sidebar with the following navigation options without breaking any existing functionality:

1. **Profile** – Open the user profile modal.
2. **Map** – Show a distance calculator between two points.
3. **User Feedback** – Present a feedback form.
4. **User Experience** – Allow photo & experience sharing.
5. **Logout** – Sign‑out the user.

---

## ✅ High‑Level Tasks

- **HTML** – Insert sidebar container and hamburger menu in `frontend/index.html`.
- **CSS** – Add premium styles (glassmorphism, smooth slide‑in, backdrop overlay) in `frontend/css/premium.css`.
- **JS** – Create `frontend/js/sidebar.js` to handle toggle, navigation, and panel switching.
- **Auth Integration** – Update `frontend/js/auth.js` to show/hide the sidebar based on login state.
- **Backend APIs** – (Optional) Stub endpoints for feedback, experiences, and map distance in the `backend/routes/` folder.

---

## 🛠️ Detailed Steps (in order)

1. **Add HTML Structure**
   - Header: `<button id="menu-toggle" class="menu-icon">☰</button>`
   - Sidebar: `<nav id="sidebar" class="sidebar hidden">` with `<ul>` containing the five `<li>` items (each with an icon and `data-panel` attribute).
   - Backdrop: `<div id="sidebar-backdrop" class="backdrop hidden"></div>`.
2. **Style the Sidebar**
   - Use `position: fixed; right: 0; top: 0; height: 100vh; width: 280px;`.
   - Apply a semi‑transparent glass effect (`background: rgba(255,255,255,0.15); backdrop-filter: blur(10px);`).
   - Animate with `transform: translateX(100%);` → `transform: translateX(0);` on open.
   - Ensure the design matches the existing app theme (dark mode, accent colors).
3. **Implement JavaScript Logic** (`sidebar.js`)
   - Toggle sidebar visibility on menu click and backdrop click.
   - Listen for clicks on navigation items; hide the sidebar and display the corresponding content panel (`#panel-profile`, `#panel-map`, etc.).
   - Add a close (X) button inside the sidebar.
4. **Integrate with Auth**
   - In `auth.js`, after successful login, add `document.getElementById('menu-toggle').style.display = 'block';`.
   - On logout, hide the menu and reset any open panels.
5. **Create Content Panels** (placeholder divs) for each option; they can be empty for now and later filled with the actual feature implementations.
6. **Testing & Verification**
   - Verify existing chat/map functionality still works.
   - Test sidebar open/close on desktop and mobile.
   - Ensure no console errors.

---

## 🚀 Success Criteria

- ✅ Sidebar slides smoothly from the right with a backdrop overlay.
- ✅ All five navigation items are clickable and switch to their respective panels.
- ✅ Sidebar only appears for logged‑in users.
- ✅ No regression in existing chat or map features.
- ✅ Visual design is premium, consistent with the rest of the app.

*Feel free to adjust the order of steps to match your development workflow.*
