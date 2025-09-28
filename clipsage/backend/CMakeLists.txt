cmake_minimum_required(VERSION 3.16)

project(WaylandClipboardManager VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6 components
find_package(Qt6 REQUIRED COMPONENTS Core Widgets Gui)

# Enable Qt MOC
set(CMAKE_AUTOMOC ON)

# Add executable
add_executable(clipboard_manager main.cpp)

# Link Qt libraries
target_link_libraries(clipboard_manager
    Qt6::Core
    Qt6::Widgets  
    Qt6::Gui
)

# Set install directory
install(TARGETS clipboard_manager DESTINATION bin)

# Create a simple .desktop file for optional system integration (only if source exists)
if(EXISTS ${CMAKE_SOURCE_DIR}/clipboard_manager.desktop.in)
    configure_file(
        ${CMAKE_SOURCE_DIR}/clipboard_manager.desktop.in
        ${CMAKE_BINARY_DIR}/clipboard_manager.desktop
        @ONLY
    )
    
    install(FILES ${CMAKE_BINARY_DIR}/clipboard_manager.desktop
            DESTINATION share/applications)
endif()
