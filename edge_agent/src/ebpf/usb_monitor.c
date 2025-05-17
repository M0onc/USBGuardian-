#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>
#include <linux/usb.h>

// eBPF Map定义
struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} usb_events SEC(".maps");

// 设备指纹结构体
struct usb_fingerprint {
    __u16 vendor;
    __u16 product;
    __u8 class;
    __u64 last_active;
};

SEC("tracepoint/usb/usb_submit_urb")
int monitor_usb(struct pt_regs *ctx) {
    struct urb *urb = (struct urb *)PT_REGS_PARM1(ctx);
    struct usb_device *udev = urb->dev;
    
    struct usb_fingerprint fp = {
        .vendor = udev->descriptor.idVendor,
        .product = udev->descriptor.idProduct,
        .class = udev->config->interface->cur_altsetting->desc.bInterfaceClass,
        .last_active = bpf_ktime_get_ns()
    };
    
    bpf_ringbuf_output(&usb_events, &fp, sizeof(fp), 0);
    return 0;
}