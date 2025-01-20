import pygame
import random
import string
import pygame.scrap  # Required for clipboard access
import pyperclip

# Initialize Pygame
pygame.init()

# Set up the display (initialize the window first)
info = pygame.display.Info()

window_height = 600
window_width = info.current_w
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption('Random Text Display with Draggable Scrollbar')

# Now initialize pygame.scrap after the window is created
pygame.scrap.init()  # Initialize Pygame's scrap for clipboard access

# Function to handle pasting from clipboard
def paste_from_clipboard():
    if pygame.scrap.get(pygame.SCRAP_TEXT) is not None:
        clipboard_data = pyperclip.paste()  # Get text from clipboard
        
        # Sanitize the text by removing null characters
        sanitized_text = clipboard_data.replace('\x00', '')  # Remove null characters
        return sanitized_text
    return ""

def display_text(screen, text, scroll_offset, max_scroll, font, num_lines):
    screen.fill((0, 100, 0))  # Clear screen with dark green background

    lines = text.splitlines()
    x, y = 20, 20 - scroll_offset
    line_height = font.get_height() + 5

    for i in range(num_lines):
        line = lines[i % len(lines)]
        words = line.split()
        x = 20  # Reset X for each line
        wrapped_line = ""  # Store wrapped line

        for word in words:
            if font.size(wrapped_line + " " + word)[0] > window_width - 40:
                # Render the wrapped line
                rendered_line = font.render(wrapped_line, True, (0, 255, 0))
                screen.blit(rendered_line, (x, y))

                # Move to the next line
                y += line_height
                wrapped_line = word  # Start new wrapped line
            else:
                wrapped_line += " " + word

        # Render the last wrapped line
        rendered_line = font.render(wrapped_line, True, (0, 255, 0))
        screen.blit(rendered_line, (x, y))

        y += line_height

    # Scrollbar rendering
    scrollbar_height = max((window_height / (num_lines * line_height)) * window_height, 20)
    scrollbar_y = (scroll_offset / max_scroll) * (window_height - scrollbar_height) if max_scroll > 0 else 0
    pygame.draw.rect(screen, (255, 255, 255), (window_width - 20, scrollbar_y, 20, scrollbar_height))

    pygame.display.flip()


# Map mouse position to scroll speed (top = no scrolling, bottom = fast scrolling)
def calculate_scroll_speed(mouse_y, window_height):
    min_speed = 0  # No scrolling when mouse is at the top
    max_speed = 2  # Slower max speed when mouse is at the bottom
    speed = min_speed + ((mouse_y / window_height) * (max_speed - min_speed))
    return speed

# Main loop
def main():
    text = paste_from_clipboard()  # Automatically paste text from clipboard on startup
    if not text:  # If no clipboard data, generate random text
        text = generate_random_words(2000)
    
    scroll_offset = 0  # Scroll offset to track how far we've scrolled
    font_size = 48
    #font = pygame.font.SysFont("SimSun-ExtG", font_size)
    font = pygame.font.SysFont("Amazon Ember", font_size)
    
    line_height = font.get_height() + 5
    num_lines = len(text.splitlines())  # Calculate the number of lines in the text
    total_text_height = num_lines * line_height  # Total height of the text

    # Adjust max_scroll to include the full text height minus the window height
    max_scroll = max(0.0000001, total_text_height - window_height)

    auto_scroll = True  # Enable auto-scrolling initially
    scroll_speed = 2  # Initial scroll speed

    scrollbar_dragging = False  # Track whether the scrollbar is being dragged
    scrollbar_height = 100

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scrollbar_y = (scroll_offset / max_scroll) * (window_height - scrollbar_height)
                # Check if clicking on the scrollbar
                if window_width - 20 <= mouse_x <= window_width and scrollbar_y <= mouse_y <= scrollbar_y + scrollbar_height:
                    scrollbar_dragging = True
                if event.button == 4:  # Mouse wheel up
                    scroll_offset = max(scroll_offset - 30, 0)
                    auto_scroll = False  # Stop auto-scrolling if user interacts
                elif event.button == 5:  # Mouse wheel down
                    scroll_offset = scroll_offset + 30
                    auto_scroll = False  # Stop auto-scrolling if user interacts
            elif event.type == pygame.MOUSEBUTTONUP:
                scrollbar_dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:  # F11 key toggles full-screen
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_UP:  # Scroll up with the UP key
                    scroll_offset = max(scroll_offset - 30, 0)
                    auto_scroll = False  # Stop auto-scrolling if user interacts
                elif event.key == pygame.K_DOWN:  # Scroll down with the DOWN key
                    scroll_offset = scroll_offset + 30
                    auto_scroll = False  # Stop auto-scrolling if user interacts
                elif event.key == pygame.K_RETURN:  # Press Enter to resume auto-scrolling
                    auto_scroll = True  # Resume auto-scrolling
                elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Ctrl+V
                    new_text = paste_from_clipboard()  # Get text from clipboard
                    if new_text:
                        text = new_text  # Replace the existing text with clipboard text
                        scroll_offset = 0  # Reset scroll position
                        num_lines = len(text.splitlines())  # Recalculate number of lines
                        total_text_height = num_lines * line_height
                        max_scroll = max(0.000001, total_text_height - window_height)  # Recalculate maximum scroll
                elif event.key == pygame.K_LEFTBRACKET:  # '[' to decrease font size
                    font_size = max(10, font_size - 2)  # Minimum font size is 10
                    font = pygame.font.SysFont("Amazon Ember", font_size)
                    line_height = font.get_height() + 5
                    num_lines = len(text.splitlines())
                    total_text_height = num_lines * line_height
                    max_scroll = max(0.000001, total_text_height - window_height)
                elif event.key == pygame.K_RIGHTBRACKET:  # ']' to increase font size
                    font_size = min(72, font_size + 2)  # Maximum font size is 72
                    font = pygame.font.SysFont("Amazon Ember", font_size)
                    line_height = font.get_height() + 5
                    num_lines = len(text.splitlines())
                    total_text_height = num_lines * line_height
                    max_scroll = max(0.000001, total_text_height - window_height)

        # Handle scrollbar dragging
        if scrollbar_dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            scroll_offset = (mouse_y / window_height) * max_scroll
            scroll_offset = max(0.000001, min(scroll_offset, max_scroll))  # Clamp scroll offset

        # Get the current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Dynamically calculate scroll speed based on mouse Y position
        scroll_speed = calculate_scroll_speed(mouse_y, window_height)

        # Auto-scroll logic
        #if auto_scroll and scroll_offset < max_scroll:
        #    scroll_offset = min(scroll_offset + scroll_speed, max_scroll)
        if auto_scroll:
            scroll_offset = scroll_offset + scroll_speed

        display_text(screen, text, scroll_offset, max_scroll, font, num_lines)
        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()
if __name__ == '__main__':
    main()
