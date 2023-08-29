import { onUnmounted } from "vue";

export function hideScrollBarWhileSwiping(
  bar: HTMLElement,
  content: HTMLElement,
) {
  let lastScrollPosition = content.scrollTop;

  const handleScroll = () => {
    const currentScrollPosition = content.scrollTop;

    if (currentScrollPosition < 50) {
      bar.classList.remove("!-translate-y-12", "shadow-lg");
      return;
    }

    if (currentScrollPosition > lastScrollPosition) {
      bar.classList.add("!-translate-y-12", "shadow-lg");
    } else {
      bar.classList.remove("!-translate-y-12");
    }

    lastScrollPosition = currentScrollPosition;
  };

  content.addEventListener("scroll", handleScroll);

  onUnmounted(() => {
    content.removeEventListener("scroll", handleScroll);
  });
}
