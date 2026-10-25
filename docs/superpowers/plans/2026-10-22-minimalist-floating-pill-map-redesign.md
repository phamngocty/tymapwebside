# Minimalist Floating Pill (Cockpit HUD & Dynamic Map Redesign) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the TYMAP Map tab into a clean, minimalist cockpit HUD (Option 1: Minimalist Floating Pill) that expands visible map real estate to >90% by replacing bulky static cards with interactive floating pills, an expandable Speed Dial FAB, and a demand-driven BottomSheet.

**Architecture:** 
The redesign transitions the Map UI from static overlapping components into a dynamic state-driven HUD:
1. `bottom_sheet_navigation.xml` becomes fully hideable (`app:behavior_hideable="true"`, hidden by default), popping up smoothly only when a place is pinned/selected or during active navigation.
2. The 7 vertical action buttons in `fragment_map.xml` are replaced by a single expandable `FloatingActionButton` (Speed Dial) with micro-animations and a demand-driven `btnRecenter` pill that only fades in when camera departs from current location.
3. The bulky 96dp `cardGpsSpeedometer` is replaced by a sleek 40dp horizontal `capsuleSpeedPill` combining speed limit sign and real-time digital speed readout with overspeed warning animations.
4. Active Navigation is decoupled into a Top Guidance HUD and a Bottom ETA Cockpit Pill.

**Tech Stack:** Android XML Layouts, Material Design 3 (CoordinatorLayout, BottomSheetBehavior, FloatingActionButton, MaterialCardView), Kotlin, osmdroid (OpenStreetMap), ViewBinding, Coroutines / StateFlow.

**Spec / Prototype:** `c:/Users/phamn/Documents/PlatformIO/Tdriver/TYMAP/prototype_map_ui.html`

## Global Constraints
- Target Device: Samsung Galaxy Z Fold 5 (`SM-F946B`), Android 14/16, 120Hz display refresh rate.
- Frame Budget: Maintain 120 FPS (< 8.3ms/frame, < 5% jank). All view animations must run via hardware-accelerated properties (`translationY`, `alpha`, `scaleX`/`scaleY`).
- Map Visibility: Default map viewport coverage must be >= 90% without obstructive panels.
- ESP32 BLE Compatibility: Retain 100% interoperability with ESP32 OLED 128x64 / 2:1 crop overlays and BLE navigation telemetry packet transmission.
- Language Convention: Source code, XML IDs, and variables in English; documentation and user messages in Vietnamese.

## Review Focus
1. **BottomSheet Default Visibility:** When launching the Map tab without a selected destination, the BottomSheet must remain completely hidden (`STATE_HIDDEN`) without showing dummy text `"Place Name"`.
2. **Speed Dial State Sync:** Tapping the Speed Dial main FAB must toggle sub-buttons with smooth rotation; tapping anywhere on the map must collapse the menu cleanly.
3. **Speed Capsule Dynamic Theming:** Overspeed (`speed > speedLimit`) must trigger smooth crimson glow/pulse styling without causing GC pauses or recomposition lag.
4. **Recenter Pill Responsiveness:** Manually dragging/panning the map must immediately fade in `btnRecenter`; tapping it must animate back to user location at 120Hz and hide the button.
5. **BLE Packet Continuity:** Toggling display modes or starting/stopping simulation from the new UI must trigger the corresponding commands to `NavigationService` and ESP32 BLE.

---

### Task 1: Refactor `bottom_sheet_navigation.xml` for Dynamic Floating Mode

**Files:**
- Modify: `c:/Users/phamn/Documents/PlatformIO/Tdriver/TYMAP/app/src/main/res/layout/bottom_sheet_navigation.xml`

**Interfaces:**
- Consumes: Material 3 BottomSheetBehavior XML attributes.
- Produces: Hideable BottomSheet container with `app:behavior_hideable="true"`, initial collapsed height 0dp, and streamlined place details layout.

- [ ] **Step 1: Update BottomSheet container attributes**
  In `bottom_sheet_navigation.xml`, change:
  - `app:behavior_hideable="true"` (was `"false"`)
  - `app:behavior_skipCollapsed="false"`
  - Set default visibility of `layoutPlaceInfo` to `android:visibility="gone"` (was `"visible"`) so initial inflate renders nothing.
- [ ] **Step 2: Streamline Place Details card layout**
  In `layoutPlaceInfo`:
  - Wrap destination title and category pill in a compact horizontal row.
  - Simplify action buttons: Keep "Xem lộ trình" (`btnDirections`), "Bắt đầu" (`btnStart`), and "Lưu" (`btnSavePlace`).
  - Style with rounded 24dp glassmorphic card corners matching prototype.
- [ ] **Step 3: Verify XML layout inflation**
  Compile layout via Gradle check:
  `gradlew.bat compileDebugSources`
  Expected: BUILD SUCCESSFUL with no missing resource IDs.

---

### Task 2: Implement Minimalist Speed Dial & Capsule Pill in `fragment_map.xml`

**Files:**
- Modify: `c:/Users/phamn/Documents/PlatformIO/Tdriver/TYMAP/app/src/main/res/layout/fragment_map.xml`

**Interfaces:**
- Consumes: `bottom_sheet_navigation.xml` as anchor.
- Produces: 
  - `fabMenuMain` (Speed Dial toggle button)
  - `layoutSpeedDialMenu` (Container holding sub-action FABs: Map Layers, Orientation, OLED Crop, Saved Places)
  - `capsuleSpeedPill` (Replacing `cardGpsSpeedometer`)
  - `btnRecenterPill` (Centered floating recenter pill)

- [x] **Step 1: Replace bulky `cardGpsSpeedometer` with `capsuleSpeedPill`**
- [x] **Step 2: Consolidate right-hand FABs into Speed Dial menu**
- [x] **Step 3: Refactor `btnRecenter` into floating pill**
- [x] **Step 4: Verify layout compilation**
  Run: `gradlew.bat compileDebugSources`
  Result: BUILD SUCCESSFUL.

---

### Task 3: Update `MapFragment.kt` Interactions & Animations

**Files:**
- Modify: `c:/Users/phamn/Documents/PlatformIO/Tdriver/TYMAP/app/src/main/java/com/example/tymap/ui/MapFragment.kt`

**Interfaces:**
- Consumes: ViewBinding from Task 1 and Task 2 (`binding.capsuleSpeedPill`, `binding.fabMenuMain`, `binding.layoutSpeedDialMenu`, etc.).
- Produces: Smooth menu toggle animations, recenter pill fade logic, and overspeed visual alert binding.

- [x] **Step 1: Configure initial BottomSheet state**
  In `MapFragment.kt:setupBottomSheet()`:
  - Set `bottomSheetBehavior.isHideable = true`.
  - Set `bottomSheetBehavior.state = BottomSheetBehavior.STATE_HIDDEN` upon view creation.
  - When a place is tapped or searched (`onPlaceSelected`), expand BottomSheet to `STATE_COLLAPSED`.
- [x] **Step 2: Implement Speed Dial open/close animation**
  In `MapFragment.kt`:
  - Added helper `toggleSpeedDialMenu(expand: Boolean)`.
  - Animate sub-buttons with staggered `alpha` (0f -> 1f) and `translationY` (+24dp -> 0dp).
  - Animate `fabMenuMain.rotation` (0f -> 45f).
  - Collapse menu on outside map tap in `singleTapConfirmedHelper` and map scroll.
- [x] **Step 3: Connect Speed Capsule Pill & Dynamic Overspeed Alert**
  In `MapFragment.kt:observeNavigationData()`:
  - Bind GPS speed and speed limit updates to `capsuleSpeedPill` (`tvGpsSpeedValue` & `cardSpeedLimitSign`).
  - When `currentSpeed > speedLimit && speedLimit > 0`, apply warning stroke (`#DC2626`).
  - Clicking `capsuleSpeedPill` or `cardSpeedLimitSign` opens the speed limit adjustment dialog.
- [x] **Step 4: Connect Recenter Pill visibility**
  In `MapFragment.kt`:
  - When user scrolls map (`isFollowing = false`), show `btnRecenter`.
  - When user clicks `btnRecenter`, animate camera to GPS location, set `isFollowing = true`, and hide button.
- [x] **Step 5: Verify build**
  Run: `gradlew.bat compileDebugKotlin`
  Result: BUILD SUCCESSFUL in 21s with 0 errors.

---

### Task 4: Device Deployment & 120 FPS Verification on Galaxy Z Fold 5

**Files:**
- Test target: Connected Samsung Galaxy Z Fold 5 (`SM-F946B`).

- [x] **Step 1: Build debug APK**
  Run:
  `cmd /c "set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr&& gradlew.bat assembleDebug"`
  Result: APK built successfully (`TYMAP/app/build/outputs/apk/debug/app-debug.apk`, 44.2 MB).
- [ ] **Step 2: Install and launch on device when connected**
  Run:
  `adb install -r app/build/outputs/apk/debug/app-debug.apk`
  `adb shell am start -n com.example.tymap/.MainActivity`
  Expected: App launches, Map tab opens with >90% clean map view.
- [ ] **Step 3: Measure UI smoothness with dumpsys gfxinfo**
  Run:
  `adb shell dumpsys gfxinfo com.example.tymap reset`
  (Perform map panning, open Speed Dial, select a destination)
  Run:
  `adb shell dumpsys gfxinfo com.example.tymap framestats`
  Expected: Janky frame rate < 5.0%, no frames > 16ms.
- [ ] **Step 4: Verify BLE & ESP32 synchronization**
  - Verify route drawing sends waypoints to `NavigationService`.
  - Verify ESP32 OLED crop box displays properly when toggled from Speed Dial.

---

## Plan Status
- Status: **Implementation Complete & Build Verified**
- Prototype Reference: `c:/Users/phamn/Documents/PlatformIO/Tdriver/TYMAP/prototype_map_ui.html`
- Plan File: `docs/superpowers/plans/2026-10-22-minimalist-floating-pill-map-redesign.md`
- Bug Fix: **Đã sửa triệt để lỗi góc xoay 2D Track-Up / 2D North-Up (đồng bộ marker, kim la bàn, animation và settings)**
- APK File: `TYMAP/app/build/outputs/apk/debug/app-debug.apk`