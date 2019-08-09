
%global golang_namespace github.com/paramite

%undefine _debugsource_packages

Name:           collectd-sensubility
Version:        0.1.1
Release:        1%{?dist}
Summary:        collectd-exec extension enabling collectd to bahave like sensu-client
License:        ASL 2.0
URL:            https://%{golang_namespace}/%{name}
Source0:        https://%{golang_namespace}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Note(mmagr): In the initial build we bundle all dependencies. To regenerate:
# curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh
# dep ensure -vendor-only
Source1:        dependencies-updated.tar.gz
Source2:        example-config.conf

BuildRequires:  gcc
BuildRequires:  golang >= 1.2-7

# Note(mmagr): Will package all libs on the run before next build
BuildRequires:  golang(github.com/go-ini/ini)
#BuildRequires:  golang(github.com/juju/errors)
#BuildRequires:  golang(github.com/rs/zerolog)
BuildRequires:  golang(github.com/streadway/amqp)
BuildRequires:  golang(github.com/stretchr/testify)

%description
This project aims provide possibility to switch from Sensu based availability monitoring solution to monitoring solution based on collectd with AMQP-1.0 messaging bus.

%prep
%autosetup -n %{name}-%{version}
# untar ./vendor directory with dependencies
tar -zxvf %{SOURCE1}

%build
# set up temporary build gopath, and put our directory there
mkdir -p ./_build/src/
mv vendor/* ./_build/src/.
mkdir -p ./_build/src/%{golang_namespace}
ln -s $(pwd) ./_build/src/%{golang_namespace}/%{name}

export GOPATH=$(pwd)/_build
#go build -o collectd-sensubility main/main.go
go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x -o collectd-sensubility main/main.go

%install
install -d %{buildroot}%{_bindir}
install -p -m 0755 ./collectd-sensubility %{buildroot}%{_bindir}/collectd-sensubility
chmod a+x %{buildroot}%{_bindir}/collectd-sensubility
install -d %{buildroot}%{_sysconfdir}
install -p -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/collectd-sensubility.conf

%files
%doc README.md
%license LICENSE
%{_bindir}/collectd-sensubility
%{_sysconfdir}/collectd-sensubility.conf

%changelog
* Fri Jul 19 2019 Martin Mágr <mmagr@redhat.com> - 0.1.1-1
- Initial build
