async function getMe() {
  const res = await fetch('/.auth/me', { credentials: 'include' });
  try {
    const payload = await res.json();
    return payload?.clientPrincipal ?? null;
  } catch {
    return null;
  }
}

async function showUser() {
  const who = document.getElementById('username');
  if (!who) return;
  const me = await getMe();
  who.textContent = me
    ? `${me.userDetails} (via ${me.identityProvider})`
    : 'Not signed in.';
}

(async () => {
  // Example: hardcoded blob; you can pick based on UI or user profile
  const blob = "test.mp4";
  const res = await fetch(`/api/video?blob=${encodeURIComponent(blob)}`, { credentials: "include" });
  if (!res.ok) {
    console.error("Failed to get SAS", res.status);
    return;
  }
  const { url } = await res.json();
  const v = document.getElementById("player");
  v.src = url;          // Point <video> directly at the SAS URL
  v.play().catch(()=>{}); // autoplay might be blocked; user can click Play
})();

showUser()