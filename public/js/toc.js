document.addEventListener("DOMContentLoaded", () => {
  const tocNavs = document.querySelectorAll(".toc ul");
  if (!tocNavs.length) return;

  const contentRoot =
    document.querySelector(".post-content") ||
    document.querySelector(".city-quake-content") ||
    document.querySelector(".dynamic-quake-content");

  if (!contentRoot) return;

  const headings = [...contentRoot.querySelectorAll("h2, h3")].filter(
    (el) => el.textContent.trim().length > 0
  );

  if (!headings.length) {
    tocNavs.forEach((toc) => {
      toc.innerHTML = "<li>Bu sayfada başlık bulunamadı.</li>";
    });
    return;
  }

  headings.forEach((heading) => {
    if (!heading.id) {
      heading.id = heading.textContent
        .trim()
        .toLowerCase()
        .replace(/[^\wığüşöçİĞÜŞÖÇ]+/g, "-")
        .replace(/^-+|-+$/g, "");
    }
  });

  const items = headings.map((heading) => {
    const level = heading.tagName === "H3" ? "sub" : "main";
    return { id: heading.id, text: heading.textContent.trim(), level };
  });

  const listHtml = items
    .map((item) => {
      const className = item.level === "sub" ? "toc-sub" : "";
      return `<li class="${className}"><a href="#${item.id}">${item.text}</a></li>`;
    })
    .join("");

  tocNavs.forEach((toc) => {
    toc.innerHTML = listHtml;
  });
});
