# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.27
# 

Name:       dracut

# >> macros
# << macros

Summary:    Initramfs generator using udev
Version:    037
Release:    1
Group:      System/Libraries
License:    GPLv2+ and LGPLv2+
URL:        https://dracut.wiki.kernel.org/
Source0:    dracut-%{version}.tar.xz
Source100:  dracut.yaml
Requires:   bash >= 4
Requires:   coreutils >= 8
Requires:   cpio
Requires:   findutils
Requires:   grep
Requires:   hardlink
Requires:   gzip
Requires:   xz
Requires:   kmod
Requires:   sed
Requires:   kpartx
Requires:   util-linux >= 2.21
Requires:   systemd >= 199
Requires:   procps
BuildRequires:  bash
BuildRequires:  systemd
Conflicts:   grubby < 8.23
Conflicts:   mdadm < 3.2.6

%description
dracut contains tools to create a bootable initramfs for 2.6 Linux kernels.
Unlike existing implementations, dracut does hard-code as little as possible
into the initramfs. dracut contains various modules which are driven by the
event-based udev. Having root on MD, DM, LVM2, LUKS is supported as well as
NFS, iSCSI, NBD, FCoE with the dracut-network package.


%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
cd upstream
# << build pre

%configure --disable-static \
    --systemdsystemunitdir=%{_libdir}/systemd/system \
    --bashcompletiondir=%{_datadir}/bash-completion \
    --libdir=%{_prefix}/lib \
    --disable-documentation

make %{?_smp_mflags}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
cd upstream
# << install pre
%make_install

# >> install post
# For systemd, better use systemd-bootchart
rm -rf %{buildroot}/%{_prefix}/lib/dracut/modules.d/00bootchart

# We don't support dash in the initramfs
rm -rf %{buildroot}/%{_prefix}/lib/dracut/modules.d/00dash

# Remove Gentoo specific modules
rm -rf %{buildroot}/%{_prefix}/lib/dracut/modules.d/50gensplash

# With systemd, IMA and selinux modules do not make sense
rm -rf %{buildroot}/%{_prefix}/lib/dracut/modules.d/96securityfs
rm -rf %{buildroot}/%{_prefix}/lib/dracut/modules.d/97masterkey
rm -rf %{buildroot}/%{_prefix}/lib/dracut/modules.d/98integrity
# << install post

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/dracut.conf
%dir %{_sysconfdir}/dracut.conf.d
%dir %{_libdir}/systemd/system/initrd.target.wants
%{_bindir}/dracut*
%{_bindir}/mkinitrd
%{_bindir}/lsinitrd
%{_datadir}/bash-completion/
%{_libdir}/dracut/
%{_libdir}/kernel/
%{_libdir}/systemd/system/*
%{_libdir}/systemd/system/shutdown.target.wants/*
# >> files
# << files
