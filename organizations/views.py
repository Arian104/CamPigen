from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json
from .models import Organization, OrganizationMembership
from accounts.models import User

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_organization(request):
    """Create a new organization (user becomes owner)"""
    try:
        data = json.loads(request.body)
        
        # Create organization
        org = Organization.objects.create(
            name=data.get('name'),
            subdomain=data.get('subdomain'),
            plan=data.get('plan', 'free'),
            owner=request.user
        )
        
        # Add owner as member
        OrganizationMembership.objects.create(
            user=request.user,
            organization=org,
            role='owner'
        )
        
        # Set as active organization
        request.user.active_organization = org
        request.user.save()
        
        return JsonResponse({
            'id': str(org.id),
            'name': org.name,
            'subdomain': org.subdomain,
            'message': 'Organization created successfully'
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_user_to_organization(request):
    """Add existing user to organization with role"""
    try:
        data = json.loads(request.body)
        org_id = data.get('organization_id')
        user_email = data.get('user_email')
        role = data.get('role', 'viewer')
        
        # Check if current user can manage users
        org = Organization.objects.get(id=org_id)
        current_user_role = OrganizationMembership.objects.get(
            user=request.user,
            organization=org
        ).role
        
        if current_user_role not in ['owner', 'admin']:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Get user to add
        user_to_add = User.objects.get(email=user_email)
        
        # Add membership
        membership, created = OrganizationMembership.objects.get_or_create(
            user=user_to_add,
            organization=org,
            defaults={'role': role}
        )
        
        return JsonResponse({
            'message': f'User {user_email} added with role {role}',
            'created': created
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def list_my_organizations(request):
    """List all organizations user belongs to"""
    memberships = OrganizationMembership.objects.filter(user=request.user)
    orgs = []
    for membership in memberships:
        orgs.append({
            'id': str(membership.organization.id),
            'name': membership.organization.name,
            'subdomain': membership.organization.subdomain,
            'role': membership.role,
            'is_active': request.user.active_organization_id == str(membership.organization.id)
        })
    return JsonResponse(orgs, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def switch_organization(request):
    """Switch user's active organization"""
    try:
        data = json.loads(request.body)
        org_id = data.get('organization_id')
        
        # Verify user is member of this organization
        membership = OrganizationMembership.objects.get(
            user=request.user,
            organization_id=org_id
        )
        
        # Update active organization
        request.user.active_organization = membership.organization
        request.user.save()
        
        return JsonResponse({
            'message': f'Switched to {membership.organization.name}',
            'organization_id': str(membership.organization.id),
            'role': membership.role
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def get_organization_members(request, org_id):
    """Get all members of an organization"""
    # Check permission
    try:
        membership = OrganizationMembership.objects.get(
            user=request.user,
            organization_id=org_id
        )
    except:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    members = OrganizationMembership.objects.filter(organization_id=org_id)
    members_list = []
    for member in members:
        members_list.append({
            'user_id': str(member.user.id),
            'email': member.user.email,
            'first_name': member.user.first_name,
            'last_name': member.user.last_name,
            'role': member.role,
            'joined_at': member.created_at
        })
    
    return JsonResponse(members_list, safe=False)
