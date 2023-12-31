from django.db import models

from worker import manage

class SSHKeys(models.Model):
    owner = models.ForeignKey("auth.User", related_name="ssh_keys", on_delete=models.PROTECT)
    label = models.CharField(max_length=32, default="default")
    pub_key = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.label} ({self.owner})"


class Access(models.Model):
    GRANTED = "GRANTED"
    REMOVED = "REMOVED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"

    STATUSES = (
        (PENDING, PENDING),
        (GRANTED, GRANTED),
        (REMOVED, REMOVED),
        (PROCESSING, PROCESSING),
        (FAILED, FAILED),
    )

    host = models.ForeignKey("hosts.Host", related_name="accesses", on_delete=models.PROTECT)
    ssh_key = models.ForeignKey(SSHKeys, related_name="accesses", on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUSES, default=PENDING)
    root_access = models.BooleanField(default=False)
    
    last_output = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.status} {self.ssh_key} - {self.host}"
    
    class Meta:
        ordering = ("-created_at", )

    def add_key_to_host(self):
        """
        Add SSH Key to host
        """
        self.status = Access.PROCESSING
        self.save()
        
        worker = manage.Worker()
        user = self.ssh_key.owner.username
        key = self.ssh_key.pub_key
        status, _, output = worker.give_access(key=key, user=user, hosts=[self.host, ], root_access=self.root_access)
        self.status = status
        self.last_output = output.decode("utf-8")
        self.save()


    def remove_key_from_host(self):
        """
        Remove SSH Key from host
        """
        self.status = Access.PROCESSING
        self.save()
        
        worker = manage.Worker()
        user = self.ssh_key.owner.username
        key = self.ssh_key.pub_key
        status, _, output = worker.remove_access(key=key, user=user, hosts=[self.host, ])
        self.status = status
        self.last_output = output.decode("utf-8")
        self.save()
    