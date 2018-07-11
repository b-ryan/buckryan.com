Title: Avoiding redundant Terraform code with loops
Date: 2018-07-10
Category:
Tags:
Author: Buck Ryan
Summary:

Terraform tip of the day: avoid redundant code with loops. This is a new-ish
feature of Terraform that didn't exist when I get started with it. An example I
just ran into was that I have an AWS Elastic Load Balancer (ELB) with several
domains pointing to it. The redundant way to write this code, and the way I had
it structured, was:

```terraform
resource "aws_route53_record" "route1" {
  zone_id = "${aws_route53_zone.my_zone.zone_id}"
  name    = "route1.foo.com"
  type    = "A"

  alias {
    name                   = "${aws_elb.my_elb.dns_name}"
    zone_id                = "${aws_elb.my_elb.zone_id}"
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "route2" {
  zone_id = "${aws_route53_zone.my_zone.zone_id}"
  name    = "route2.foo.com"
  type    = "A"

  alias {
    name                   = "${aws_elb.my_elb.dns_name}"
    zone_id                = "${aws_elb.my_elb.zone_id}"
    evaluate_target_health = false
  }
}

...
```

But if you have more than 2 resources doing the same thing, the code really
gets lengthy. Without going into all the details, here's the looping version:

```
variable "all_subdomains" {
  default = ["route1", "route2"]
}

resource "aws_route53_record" "elb_routes" {
  count   = "${length(var.all_subdomains)}"
  zone_id = "${aws_route53_zone.my_zone.zone_id}"
  name    = "${element(var.all_subdomains, count.index)}.foo.com"
  type    = "A"

  alias {
    name                   = "${aws_elb.my_elb.dns_name}"
    zone_id                = "${aws_elb.my_elb.zone_id}"
    evaluate_target_health = false
  }
}
```

## Downsides

It's not all rosy though. Be aware that you can't change the ordering of the
items in your variable or else resources will be re-created. For example, if
these routes existed and I added a new subdomain to the beginning, like

```
variable "all_subdomains" {
  default = ["new", "route1", "route2"]
}
```

This would cause the `route1` and `route2` records to be deleted and created
again. This can be dangerous and should be avoided.

Additionally, if you need a particular resource to depend on one of these
routes, you must use the index of the resource rather than being able to refer
to it by name. For example:

```
output "route1_name" {
  value = "${aws_route53_record.elb_routes.0.name}"
}
```
