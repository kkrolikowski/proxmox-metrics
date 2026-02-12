// Source - https://stackoverflow.com/a/54064268
// Posted by Paul Wasilewski, modified by community. See post 'Timeline' for change history
// Retrieved 2026-02-08, License - CC BY-SA 4.0

db.createUser({
  user: "root",
  pwd: "superSecret",
  roles: [
    {
      role: "readWrite",
      db: "proxmox-metrics",
    },
  ],
});
