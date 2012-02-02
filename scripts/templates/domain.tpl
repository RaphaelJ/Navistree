zone "{domain}" IN {{
        type master;
        file "{zone}";
        allow-update {{ none; }};
        notify no;
}};
