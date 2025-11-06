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

showUser()